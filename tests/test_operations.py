import unittest

from colorize import Colorize


class TestOperations(unittest.TestCase):
    def test_add(self) -> None:
        a = Colorize("Red").red()
        b = Colorize("Blue").blue()

        self.assertEqual(a + b, "\033[31mRed\033[39m\033[34mBlue\033[39m")
        self.assertEqual(a + "\n", "\033[31mRed\033[39m\n")
        world = Colorize("World").yellow()
        self.assertEqual(
            "Hello, " + world + "!",
            "Hello, \033[33mWorld\033[39m!",
        )

    def test_eq(self) -> None:
        a = Colorize("Red").red()
        b = Colorize("Blue").blue()

        self.assertTrue(a == "\033[31mRed\033[39m")
        self.assertFalse(a == b)
