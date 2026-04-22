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


def test_cli_story_001_s1_valid_reveal_command_parsed_and_dispatched():
    # GIVEN - the CLI is running with no mines so (2, 3) is always safe
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters "r 2 3" then "q"
    result = subprocess.run(
        [
            sys.executable,
            "minesweeper/cli.py",
            "--rows",
            "5",
            "--cols",
            "5",
            "--mines",
            "0",
        ],
        input="r 2 3\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - board re-renders after reveal, process exits 0
    assert result.returncode == 0, result.stderr
    # Two board renders: initial (5 rows) + after reveal (5 rows) = 10 lines
    assert len(result.stdout.splitlines()) >= 10


def test_cli_story_001_s2_valid_flag_command_parsed_and_dispatched():
    # GIVEN - the CLI is running
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters "f 1 4" then "q"
    result = subprocess.run(
        [
            sys.executable,
            "minesweeper/cli.py",
            "--rows",
            "5",
            "--cols",
            "5",
            "--mines",
            "0",
        ],
        input="f 1 4\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - board re-renders with F at row 1 col 4, process exits 0
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    # Second board starts at line 5 (0-indexed); row 1 of second board is line 6
    assert any(ln.split() and ln.split()[4] == "F" for ln in lines)


def test_cli_story_001_s3_invalid_input_prints_usage_hint_and_continues():
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

    # THEN - usage hint printed, no traceback, process exits 0
    assert result.returncode == 0, result.stderr
    assert "Usage: r <row> <col> | f <row> <col> | q" in result.stdout
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr


def test_cli_story_001_s4_quit_command_exits_cleanly():
    # GIVEN - the CLI is running
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters "q"
    result = subprocess.run(
        [sys.executable, "minesweeper/cli.py", "--seed", "42"],
        input="q\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - process exits with code 0, no traceback
    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stdout
    assert "Traceback" not in result.stderr
