import builtins
from optparse import OptionParser
from typing import FrozenSet, Generator, List, Set, Tuple

from flake8_variables_names import __version__ as version
from flake8_variables_names.ast_helpers import extract_all_variable_names

ErrorTuple = Tuple[int, int, str, type]


class VariableNamesChecker:
    name = 'flake8-variables-names'
    version = version

    use_strict_mode = False

    allow_variable_names: Set[str] = set()
    custom_bad_names: Set[str] = set()

    _variable_names_blacklist = frozenset((
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
    ))
    _variable_names_blacklist_strict_addon = frozenset((
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
    ))
    _single_letter_names_whitelist = frozenset(('i', '_', 'T'))
    _single_letter_names_whitelist_strict = frozenset(('_', 'T'))

    __cached_blacklist: Set[str] = set()

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    @property
    def single_letter_names_whitelist(self) -> FrozenSet[str]:
        return (
            self._single_letter_names_whitelist_strict
            if self.use_strict_mode
            else self._single_letter_names_whitelist
        )

    @property
    def variable_names_blacklist(self) -> Set[str]:
        if self.__cached_blacklist:
            return self.__cached_blacklist

        names: Set[str] = set(self._variable_names_blacklist)

        if self.use_strict_mode:
            names |= self._variable_names_blacklist_strict_addon

        names |= self.custom_bad_names
        names -= self.allow_variable_names

        self.__cached_blacklist = names

        return self.__cached_blacklist

    @classmethod
    def add_options(cls, parser: OptionParser) -> None:
        parser.add_option(
            '--use-varnames-strict-mode',
            action='store_true',
        )
        parser.add_option(
            '--add-bad-varnames',
            type=str,
            action='append',
            parse_from_config=True,
            default=[],
        )
        parser.add_option(
            '--allow-varnames',
            type=str,
            action='append',
            parse_from_config=True,
            default=[],
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.use_strict_mode = bool(options.use_varnames_strict_mode)

        if isinstance(options.add_bad_varnames, str):
            varnames = options.add_bad_varnames.split(',')
            cls.custom_bad_names = {varname.strip() for varname in varnames}
        else:
            cls.custom_bad_names = set(options.add_bad_varnames)

        if isinstance(options.allow_varnames, str):
            varnames = options.allow_varnames.split(',')
            cls.allow_variable_names = {varname.strip() for varname in varnames}
        else:
            cls.allow_variable_names = set(options.allow_varnames)

    def run(self) -> Generator[ErrorTuple, None, None]:
        variables_names = extract_all_variable_names(self.tree)
        for var_name, var_name_ast_node in variables_names:
            errors = self.get_varname_errors(var_name, var_name_ast_node)
            for error in errors:
                yield (*error, type(self))

    def get_varname_errors(self, var_name: str, var_ast_node) -> List[Tuple[int, int, str]]:
        errors = []
        buildin_names = dir(builtins)
        if (
            len(var_name) == 1
            and var_name not in self.single_letter_names_whitelist
        ):
            errors.append((
                var_ast_node.lineno,
                var_ast_node.col_offset,
                "VNE001 single letter variable names like '{0}' are not allowed".format(var_name),
            ))
        if var_name in self.variable_names_blacklist:
            errors.append((
                var_ast_node.lineno,
                var_ast_node.col_offset,
                "VNE002 variable name '{0}' should be clarified".format(var_name),
            ))
        if var_name in buildin_names:
            errors.append((
                var_ast_node.lineno,
                var_ast_node.col_offset,
                'VNE003 variable names that shadow builtins are not allowed',
            ))

        return errors
