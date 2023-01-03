import ast
import inspect
from flake8_unused_globals import Plugin


def test_no_unused() -> None:
    source = inspect.cleandoc("""
        B = 6

        def f() -> int:
            return B
    """)
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    assert result == []


def test_one_unused() -> None:
    source = inspect.cleandoc("""
        A = 5
        B = 6

        def f() -> int:
            return B
    """)
    plugin = Plugin(ast.parse(source))
    result = list(plugin.run())

    expected = [
        (1, 0, "UUG001 Unused global variable 'A'", "unused global variable")
    ]
    assert result == expected
