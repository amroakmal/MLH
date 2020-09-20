import sys
import os
import shlex
import subprocess
import difflib
from pathlib import Path
from .lib import compile_submission as compiler
from .lib import compute_results as compute_results
from .lib import test_cases_parser as tc_parser
from .lib.submissions_extraction import extract_submissions, clean_directory
import json


def get_lab_path(course, lab):
    return Path(__file__).joinpath(
        f'../../../courses/{course}/labs/{lab}').resolve()


def run_grader(course, lab):
    """
    Compiles all the submissions in [lab_path/submissions/] directory, runs compiled submissions
    with stdin of the lab's test cases, then builds a dictionary that has all the submissions 
    with the submissions id as the key and the results of this submissions as the value 
    example dictionray:
    {
        "3245_3213": {
            "passed": [1, 3, 5 , 7],
            "failed": [
                {"tc_id": "2", "diff": *DIFF TEXT*}, 
                {"tc_id": "4", "diff": *DIFF TEXT*}, 
                {"tc_id": "6", "diff": *DIFF TEXT*}]
        },
        "2136_2315": {
            "passed": [1, 2, 3, 5, 6, 7],
            "failed": [
                {"tc_id": "4", "diff": *DIFF TEXT*}, 
        }
    }
    """
    LAB_ABS_PATH = get_lab_path(course, lab)
    test_cases = tc_parser.get_test_cases(LAB_ABS_PATH)
    submission_result_list = []

    # Looping over all the submissions in [lab_path/submissions/] directory, first compile the submission
    # then loop over all test_cases for this lab, run the compiled submissions with stdin of the test case input
    # then compare it to the test case output, if both matched add the test case id to the "passed" array
    # if not add the test case id along with the diff between outout and test case expected output to "failed" array
    for _, dir, _ in os.walk(LAB_ABS_PATH.joinpath(f"submissions")):
        for i in dir:
            submission_dir = str(
                LAB_ABS_PATH.joinpath(f"submissions")) + f"/{i}"
            compiler.compile_submission(Path(submission_dir))

            current_submission = {
                "id": i,
                "passed": [],
                "failed": []
            }
            for tc in test_cases:
                exec_command = f"./a.out"
                cmd = shlex.split(exec_command)
                cprocess = subprocess.run(
                    cmd, input=tc[1], cwd=submission_dir, capture_output=True, text=True)
                differences = ""
                for line in difflib.context_diff(cprocess.stdout, tc[2]):
                    differences += line + "\n"
                if(len(differences) == 0):
                   current_submission["passed"].append(tc[0])
                else:
                    student_output = ""
                    if cprocess.returncode != 0:
                        student_output = "ERROR"
                    else:
                        student_output = cprocess.stdout
                    current_submission["failed"].append({
                        "tc_id": tc[0],
                        "output": student_output,
                        "expected": tc[2]
                    })
            submission_result_list.append(current_submission)
                
    # compute_total_result will take the results dict then create results files in the lab's directory
    compute_results.compute_total_result(submission_result_list, LAB_ABS_PATH)
