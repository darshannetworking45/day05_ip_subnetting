
import importlib
import shutil
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS))
import harness as h  


def main():
    modules = sorted(TESTS.glob("test_day*.py"))
    if not modules:
        sys.exit("No test_dayNN.py files found.")
    for path in modules:
        print(f"\n== {path.stem} ==")
        try:
            importlib.import_module(path.stem).run(h)
        except AssertionError as exc:
            h.FAILED.append(f"{path.stem}: {exc}")
            print("FAIL ", exc)
    shutil.rmtree(h.TEST_OUTPUT, ignore_errors=True)       
    print("\nRESULT:", "ALL TESTS PASSED" if not h.FAILED else f"FAILED: {h.FAILED}")
    return 1 if h.FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
