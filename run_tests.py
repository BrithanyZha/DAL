"""
Run tests for Herding Cats (ICPC WF 2023 Problem F)
- Windows friendly (no ANSI colors)
- Uses sys.executable
- Includes detailed description of test case conditions
"""

import subprocess
import time
import os
import sys

def run_one(test_file: str):
    start = time.perf_counter()

    with open(test_file, "r", encoding="utf-8") as f:
        p = subprocess.run(
            [sys.executable, "solution.py"],
            stdin=f,
            capture_output=True,
            text=True,
            timeout=10
        )

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    out = (p.stdout or "").strip().replace("\r\n", "\n")
    err = (p.stderr or "").strip()

    if p.returncode != 0:
        return False, elapsed_ms, out, f"RUNTIME ERROR:\n{err}"

    return True, elapsed_ms, out, ""

def main():
    # TEST CASES dengan deskripsi kondisi input
    tests = [
        {
            "file": "test_input_1.txt",
            "expected": "yes\nno",
            "description": "Sample dari ICPC Problem Statement (2 test cases)",
            "condition": "Case 1: [3 cats, 5 pots] - Solvable (Valid arrangement exists)",
            "subcondition": "Case 2: [3 cats, 5 pots] - Impossible (Last cat targets pot 5, conflicts)"
        },
        {
            "file": "test_input_2.txt",
            "expected": "yes",
            "description": "Simple Valid Case",
            "condition": "3 cats, 3 pots - Each cat targets different pot",
            "subcondition": "Each cat likes unique plant (no conflicts) - Lintasan Lurus"
        },
        {
            "file": "test_input_3.txt",
            "expected": "no",
            "description": "Impossible Case - Plant Conflict",
            "condition": "4 cats, 6 pots - Multiple cats want different pots",
            "subcondition": "Pot 1 is non-target but all plants are liked - No safe plant for pot 1"
        },
        {
            "file": "test_input_4.txt",
            "expected": "no",
            "description": "Impossible Case - No Safe Plant",
            "condition": "6 cats, 8 pots - Complex preferences",
            "subcondition": "Pot 1 is non-target but all 8 plants are used by cats - Impossible to fill"
        },
        {
            "file": "test_input_5.txt",
            "expected": "no\nno",
            "description": "Mixed Cases (2 test cases)",
            "condition": "Case 1: [4 cats, 5 pots] - Pot 1 non-target, all plants liked",
            "subcondition": "Case 2: [5 cats, 6 pots] - Pot 1 non-target, all plants liked"
        }
    ]

    print("=" * 100)
    print("Herding Cats - Test Runner with Detailed Conditions")
    print("=" * 100)

    passed = 0
    total_ms = 0.0

    for i, test_info in enumerate(tests, 1):
        fname = test_info["file"]
        expected = test_info["expected"]
        description = test_info["description"]
        condition = test_info["condition"]
        subcondition = test_info["subcondition"]

        print(f"\nTest {i}: {fname}")
        print(f"  Description : {description}")
        print(f"  Condition   : {condition}")
        print(f"  Detail      : {subcondition}")

        if not os.path.exists(fname):
            print(f"  Status      : FAIL (file not found)")
            continue

        ok_run, ms, out, err = run_one(fname)
        total_ms += ms

        expected_clean = expected.strip().replace("\r\n", "\n")
        out_clean = out.strip().replace("\r\n", "\n")

        ok_match = (out_clean == expected_clean)
        status = "PASS" if (ok_run and ok_match) else "FAIL"

        print(f"  Status      : {status}")
        print(f"  Runtime     : {ms:.2f} ms")
        print(f"  Output      : {out_clean.replace(chr(10), ' | ')}")
        print(f"  Expected    : {expected_clean.replace(chr(10), ' | ')}")

        if err:
            print(f"  Error       : {err}")

        if status == "PASS":
            passed += 1

    # --- SUMMARY SECTION ---
    num_tests = len(tests)
    avg_ms = total_ms / num_tests if num_tests > 0 else 0.0

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Passed        : {passed}/{num_tests}")
    print(f"Total Runtime : {total_ms:.2f} ms")
    print(f"Avg Runtime   : {avg_ms:.2f} ms")
    print("Time Limit    : 2000 ms (2 seconds)")
    
    if total_ms < 2000:
        print("Status        : SAFE - All tests completed within time limit")
    else:
        print("Status        : WARNING - Total runtime exceeds time limit")
    
    if passed == num_tests:
        print("Result        : ALL TESTS PASSED ✓")
    else:
        print(f"Result        : {num_tests - passed} test(s) failed")
    
    print("=" * 100)

if __name__ == "__main__":
    main()