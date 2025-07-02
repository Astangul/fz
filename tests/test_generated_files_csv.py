import sys
import types
import csv
import os

module = types.ModuleType("rpy2")
class DummyR:
    def assign(self, name, val):
        pass
    def __call__(self, code):
        return [0]
robjects = types.SimpleNamespace(r=DummyR())
module.robjects = robjects
sys.modules['rpy2'] = module
sys.modules['rpy2.robjects'] = robjects

from fz import fz


def test_generated_files_csv(tmp_path):
    input_file = tmp_path / "in.txt"
    input_file.write_text("simple")
    f = fz()
    f.CompileInput(str(input_file), input_variables={"x": [1, 2]})

    csv_path = tmp_path / "generated_files.csv"
    assert csv_path.exists()
    with open(csv_path, newline="") as cf:
        rows = list(csv.DictReader(cf))
    assert len(rows) == 2
    expected_path = os.path.relpath(os.getcwd(), start=tmp_path)
    assert rows[0]["path"] == expected_path
    assert rows[0]["file"].endswith("in_x=1.txt")
    assert rows[0]["x"] == "1"
    assert rows[1]["path"] == expected_path
    assert rows[1]["file"].endswith("in_x=2.txt")
    assert rows[1]["x"] == "2"
