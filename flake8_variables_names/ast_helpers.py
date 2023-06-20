import ast
import functools
from typing import List, Tuple, Union

from flake8_variables_names.list_helpers import flat


@functools.singledispatch
def extract_names_from_node(node) -> List[ast.Name]:
    return []


@extract_names_from_node.register
def _extract_names_from_name_node(node: ast.Name) -> List[ast.Name]:
    return [node]


@extract_names_from_node.register
def _extract_names_from_assign_node(node: ast.Assign) -> List[ast.Name]:
    return flat([extract_names_from_node(target) for target in node.targets])


# in some versions of Python, singledispatch does not support `Union` in type annotations
@extract_names_from_node.register(ast.AnnAssign)
@extract_names_from_node.register(ast.For)
def _extract_names_from_annassign_node(node) -> List[ast.Name]:
    return extract_names_from_node(node.target)


@extract_names_from_node.register
def _extract_names_from_starred_node(node: ast.Starred) -> List[ast.Name]:
    return extract_names_from_node(node.value)


@extract_names_from_node.register
def _extract_names_from_tuple_node(node: ast.Tuple) -> List[ast.Name]:
    return flat([extract_names_from_node(elt) for elt in node.elts])


def get_var_names_from_assignment(
    assignment_node: Union[ast.Assign, ast.AnnAssign, ast.For],
) -> List[Tuple[str, ast.AST]]:
    return [(n.id, n) for n in extract_names_from_node(assignment_node)]


def get_var_names_from_funcdef(funcdef_node: ast.FunctionDef) -> List[Tuple[str, ast.arg]]:
    vars_info = []
    for arg in funcdef_node.args.args:
        vars_info.append(
            (arg.arg, arg),
        )
    return vars_info


def extract_all_variable_names(ast_tree: ast.AST) -> List[Tuple[str, ast.AST]]:
    var_info: List[Tuple[str, ast.AST]] = []
    assignments = [
        n for n in ast.walk(ast_tree)
        if isinstance(n, (ast.Assign, ast.AnnAssign, ast.For))
    ]
    var_info += flat([get_var_names_from_assignment(a) for a in assignments])
    funcdefs = [n for n in ast.walk(ast_tree) if isinstance(n, ast.FunctionDef)]
    var_info += flat([get_var_names_from_funcdef(f) for f in funcdefs])
    return var_info
