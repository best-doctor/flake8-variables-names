import ast
import os
from typing import Optional

from flake8_variables_names.checker import VariableNamesChecker, ErrorTuple


def run_validator_for_test_file(filename: str, use_strict_mode: Optional[bool] = None):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = VariableNamesChecker(tree=tree, filename=filename)
    if use_strict_mode is not None:
        checker.use_strict_mode = use_strict_mode

    return list(checker.run())


def get_error_message(error: ErrorTuple) -> str:
    ''' Get error message from error tuple returned by VariableNamesChecker.run() '''
    return error[2]
