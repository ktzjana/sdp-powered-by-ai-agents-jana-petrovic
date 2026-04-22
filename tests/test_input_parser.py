# Input parsing tests — CLI-BE-001.1-S1 and later scenarios
from minesweeper.input_parser import InputParser


def test_cli_be_001_1_s1_parse_returns_reveal_command():
    # GIVEN - the raw input string is "r 2 3"

    # WHEN
    cmd = InputParser.parse("r 2 3")

    # THEN
    assert cmd.action == "reveal"
    assert cmd.row == 2
    assert cmd.col == 3


def test_cli_be_001_1_s2_parse_returns_flag_command():
    # GIVEN - the raw input string is "f 1 4"

    # WHEN
    cmd = InputParser.parse("f 1 4")

    # THEN
    assert cmd.action == "flag"
    assert cmd.row == 1
    assert cmd.col == 4


def test_cli_be_001_1_s3_parse_returns_quit_command():
    # GIVEN - the raw input string is "q"

    # WHEN
    cmd = InputParser.parse("q")

    # THEN
    assert cmd.action == "quit"
    assert cmd.row is None
    assert cmd.col is None


def test_cli_be_001_1_s4_parse_raises_for_invalid_input():
    # GIVEN - invalid input strings

    import pytest

    # WHEN / THEN - ValueError is raised for unrecognised input
    with pytest.raises(ValueError):
        InputParser.parse("xyz")

    with pytest.raises(ValueError):
        InputParser.parse("r abc")


def test_cli_fe_001_1_s1_usage_hint_printed_for_unrecognised_input():
    # GIVEN - the CLI is running
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters "xyz" (invalid) then "q"
    result = subprocess.run(
        [sys.executable, "minesweeper/cli.py", "--seed", "42"],
        input="xyz\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - usage hint is printed once and q exits cleanly
    assert result.returncode == 0, result.stderr
    usage = "Usage: r <row> <col> | f <row> <col> | q"
    assert result.stdout.count(usage) == 1


def test_cli_fe_001_1_s2_no_usage_hint_for_valid_command():
    # GIVEN - the CLI is running
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters a valid flag command then q
    result = subprocess.run(
        [sys.executable, "minesweeper/cli.py", "--seed", "42"],
        input="f 0 0\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - no usage hint is printed; board renders with F visible
    assert result.returncode == 0, result.stderr
    usage = "Usage: r <row> <col> | f <row> <col> | q"
    assert usage not in result.stdout
    assert "F" in result.stdout
