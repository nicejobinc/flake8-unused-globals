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
    result = plugin.run()

    assert result == []


def test_one_unused() -> None:
    source = inspect.cleandoc("""
        A = 5
        B = 6

        def f() -> int:
            return B
    """)
    plugin = Plugin(ast.parse(source))
    result = plugin.run()

    expected = [
        (1, 0, "UUG001 Unused global variable 'A'", "unused global variable")
    ]
    assert result == expected


def test_unused_at_eof_not_flagged() -> None:
    source = inspect.cleandoc("""
        A = 5

        def f() -> None:
            return

        B = 6
    """)
    plugin = Plugin(ast.parse(source))
    result = plugin.run()

    expected = [
        (1, 0, "UUG001 Unused global variable 'A'", "unused global variable")
    ]
    assert result == expected


def test_constants_file_not_flagged_some_annotated() -> None:
    source = inspect.cleandoc("""
        STRINGS = ["A", "B"]
        NUMBER: int = 5
        FLOATING_NUMBER: float = 5.0
    """)
    plugin = Plugin(ast.parse(source))
    result = plugin.run()

    assert result == []
