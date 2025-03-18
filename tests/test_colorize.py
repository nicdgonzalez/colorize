import unittest

from colorize import Colorize


# fmt: off
class TestColorize(unittest.TestCase):
    def test_foreground(self) -> None:
        self.assertEqual(str(Colorize("foo").black()), "\033[30mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").red()), "\033[31mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").green()), "\033[32mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").yellow()), "\033[33mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").blue()), "\033[34mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").magenta()), "\033[35mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").cyan()), "\033[36mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").white()), "\033[37mfoo\033[39m")
        self.assertEqual(str(Colorize("foo").color256(219)), "\033[38;5;219mfoo\033[39m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").true_color(255, 0, 0)), "\033[38;2;255;0;0mfoo\033[39m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").true_color(0, 128, 0)), "\033[38;2;0;128;0mfoo\033[39m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").true_color(0, 0, 72)), "\033[38;2;0;0;72mfoo\033[39m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").true_color(50, 0, 100)), "\033[38;2;50;0;100mfoo\033[39m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").true_color(3, 6, 9)), "\033[38;2;3;6;9mfoo\033[39m")  # noqa: E501

    def test_background(self) -> None:
        self.assertEqual(str(Colorize("foo").on_black()), "\033[40mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_red()), "\033[41mfoo\033[49m")
        self.assertEqual(str(Colorize("foo").on_green()), "\033[42mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_yellow()), "\033[43mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_blue()), "\033[44mfoo\033[49m")
        self.assertEqual(str(Colorize("foo").on_magenta()), "\033[45mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_cyan()), "\033[46mfoo\033[49m")
        self.assertEqual(str(Colorize("foo").on_white()), "\033[47mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_color256(219)), "\033[48;5;219mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_true_color(255, 0, 0)), "\033[48;2;255;0;0mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_true_color(0, 128, 0)), "\033[48;2;0;128;0mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_true_color(0, 0, 72)), "\033[48;2;0;0;72mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_true_color(50, 0, 100)), "\033[48;2;50;0;100mfoo\033[49m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").on_true_color(3, 6, 9)), "\033[48;2;3;6;9mfoo\033[49m")  # noqa: E501

    def test_style(self) -> None:
        self.assertEqual(str(Colorize("foo")), "foo")
        self.assertEqual(str(Colorize("foo").bold()), "\033[1mfoo\033[22m")
        self.assertEqual(str(Colorize("foo").dim()), "\033[2mfoo\033[22m")
        self.assertEqual(str(Colorize("foo").italic()), "\033[3mfoo\033[23m")
        self.assertEqual(str(Colorize("foo").underline()), "\033[4mfoo\033[24m")  # noqa: E501
        self.assertEqual(str(Colorize("foo").blink()), "\033[5mfoo\033[25m")
        self.assertEqual(str(Colorize("foo").inverse()), "\033[7mfoo\033[27m")
        self.assertEqual(str(Colorize("foo").hidden()), "\033[8mfoo\033[28m")
        self.assertEqual(str(Colorize("foo").strikethrough()), "\033[9mfoo\033[29m")  # noqa: E501

    def test_combo(self) -> None:
        self.assertEqual(str(Colorize("foo").bold().red()), "\033[1;31mfoo\033[22;39m")  # noqa: E501

    def test_nested(self) -> None:
        self.assertEqual(
            str(Colorize(f"What is {Colorize("your").italic()} name?").cyan()),
            "\033[36mWhat is \033[3myour\033[23m name?\033[39m"
        )
# fmt: on
