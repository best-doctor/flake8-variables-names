from optparse import OptionParser
from typing import Generator, Tuple, List

from flake8_variables_names import __version__ as version
from flake8_variables_names.ast_helpers import extract_all_variable_names


class VariableNamesChecker:
    name = 'flake8-variables-names'
    version = version

    use_strict_mode = False

    _variable_names_blacklist = [
        # from https://github.com/wemake-services/wemake-python-styleguide/
        'val',
        'vals',
        'var',
        'vars',
        'variable',
        'contents',
        'handle',
        'file',
        'objs',
        'some',
        'do',
        'no',
        'true',
        'false',
        'foo',
        'bar',
        'baz',
    ]
    _variable_names_blacklist_strict_addon = [
        'data',
        'result',
        'results',
        'item',
        'items',
        'value',
        'values',
        'content',
        'obj',
        'info',
        'handler',
    ]
    _single_letter_names_whitelist = ['i', '_', 'T']
    _single_letter_names_whitelist_strict = ['_', 'T']

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        variables_names = extract_all_variable_names(self.tree)
        for var_name, var_name_ast_node in variables_names:
            errors = self.get_varname_errors(var_name, var_name_ast_node)
            for error in errors:
                yield (*error, type(self))

    def get_varname_errors(self, var_name: str, var_ast_node) -> List[Tuple[int, int, str]]:
        errors = []
        if (
            len(var_name) == 1
            and var_name not in self.single_letter_names_whitelist
        ):
            errors.append((
                var_ast_node.lineno,
                var_ast_node.col_offset,
                'VNE001 single letter variable names are not allowed',
            ))
        if var_name in self.variable_names_blacklist:
            errors.append((
                var_ast_node.lineno,
                var_ast_node.col_offset,
                'VNE002 variable name should be clarified',
            ))
        return errors

    @classmethod
    def add_options(cls, parser: OptionParser) -> None:
        parser.add_option(
            '--use-varnames-strict-mode',
            action='store_true',
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.use_strict_mode = bool(options.use_varnames_strict_mode)

    @property
    def single_letter_names_whitelist(self) -> List[str]:
        return (
            self._single_letter_names_whitelist_strict
            if self.use_strict_mode
            else self._single_letter_names_whitelist
        )

    @property
    def variable_names_blacklist(self) -> List[str]:
        if self.use_strict_mode:
            return self._variable_names_blacklist + self._variable_names_blacklist_strict_addon
        else:
            return self._variable_names_blacklist
