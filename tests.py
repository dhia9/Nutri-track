#!/usr/bin/env python3
"""
Test runner for nutritrack project.
Discovers and runs all test functions from src/tests/*.py files.
"""

import sys
import importlib
import inspect
from pathlib import Path
from io import StringIO


def discover_and_run_tests():
    """Discover and run all test functions in src/tests."""
    tests_dir = Path("src") / "tests"

    # Include both test_*.py and utility files like accent_rm.py and menu_generator.py
    all_test_files = sorted(tests_dir.glob("test_*.py"))
    all_test_files.extend(sorted(tests_dir.glob("accent_rm.py")))
    all_test_files.extend(sorted(tests_dir.glob("menu_generator.py")))

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    errors = []

    print("\n" + "=" * 60)
    print("  NUTRITRACK TEST RUNNER")
    print("=" * 60)

    for test_file in all_test_files:
        module_name = f"src.tests.{test_file.stem}"
        try:
            module = importlib.import_module(module_name)

            # Find all test functions in the module
            test_functions = [
                (name, func)
                for name, func in inspect.getmembers(module)
                if name.startswith("test_")
                and callable(func)
                and not name.startswith("test_print")
            ]

            if test_functions:
                print(f"\n{test_file.name}:")

                for test_name, test_func in test_functions:
                    total_tests += 1
                    try:
                        # Capture print output to detect True/False
                        captured_output = StringIO()
                        sys.stdout = captured_output
                        test_func()
                        sys.stdout = sys.__stdout__

                        output = captured_output.getvalue().strip()
                        if output == "True":
                            print(f"  ✓ {test_name}")
                            passed_tests += 1
                        else:
                            print(f"  ✗ {test_name}")
                            failed_tests += 1
                    except Exception as e:
                        sys.stdout = sys.__stdout__
                        failed_tests += 1
                        errors.append(
                            {"file": test_file.name, "test": test_name, "error": str(e)}
                        )
                        print(f"  ✗ {test_name}")
        except Exception as e:
            print(f"   Error importing {module_name}: {e}")
            errors.append({"file": test_file.name, "test": "import", "error": str(e)})

    # Print summary
    print("\n" + "=" * 60)
    print("  RÉSUMÉ FINAL")
    print("=" * 60)
    print(f"Total:     {total_tests}")
    print(f"Réussis:   {passed_tests}")
    print(f"Échoués:   {failed_tests}")
    if total_tests > 0:
        print(f"Taux:      {passed_tests / total_tests * 100:.1f}%")

    if errors:
        print("\n" + "=" * 60)
        print("  ERREURS")
        print("=" * 60)
        for error in errors:
            print(f"\n {error['file']}::{error['test']}")
            print(f"   {error['error']}")

    print("\n" + "=" * 60 + "\n")

    # Exit with appropriate code
    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    exit_code = discover_and_run_tests()
    sys.exit(exit_code)
