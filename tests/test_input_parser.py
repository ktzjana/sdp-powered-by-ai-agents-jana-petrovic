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
