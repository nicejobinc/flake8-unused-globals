import ast
from typing import Iterable, Any

ERROR_CODE = "UUG001"
CHECK = "unused global variable"
E = 0


with open("__VERSION__") as f:
    VERSION = f.read().strip()


class GlobalVariableLoadCounter(ast.NodeVisitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.id_to_loads = {}
        self.id_to_store_info = {}

    def visit_Name(self, name: ast.Name) -> None:
        if isinstance(name.ctx, ast.Load) and name.id in self.id_to_loads:
            self.id_to_loads[name.id] += 1
        elif isinstance(name.ctx, ast.Store):
            self.id_to_loads[name.id] = 0
            self.id_to_store_info[name.id] = {
                "end_lineno": name.end_lineno,
                "col_offset": name.col_offset
            }


class Plugin:
    name = "flake8-unused-globals"
    version = VERSION

    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree

    @property
    def global_variables(self) -> set[str]:
        return {
            target.id
            for assignment in self.tree.body
            if isinstance(assignment, ast.Assign)
            for target in assignment.targets
            if isinstance(target, ast.Name)
        }

    def run(self) -> Iterable[tuple[int, int, str, str]]:
        load_counter = GlobalVariableLoadCounter()
        load_counter.visit(self.tree)

        for id_, loads in load_counter.id_to_loads.items():
            if id_ in self.global_variables and loads == 0:
                store_info = load_counter.id_to_store_info[id_]
                text = f"{ERROR_CODE} Unused global variable '{id_}'"
                yield (
                    store_info["end_lineno"],
                    store_info["col_offset"],
                    text,
                    CHECK
                )
