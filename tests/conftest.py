import ast
import os

from flake8_variables_names.checker import ErrorTuple, VariableNamesChecker


def run_validator_for_test_file(filename: str, **kwargs):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = VariableNamesChecker(tree=tree, filename=filename)

    for attr_name, attr_value in kwargs.items():
        setattr(checker, attr_name, attr_value)

    return list(checker.run())


def get_error_message(error: ErrorTuple) -> str:
    """Get error message from error tuple returned by `VariableNamesChecker.run()`."""
    return error[2]
