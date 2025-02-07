from __future__ import annotations

import os
import sys
from typing import Callable, Self

__all__ = ("Colorize",)

NO_COLOR = os.getenv("NO_COLOR", False)
FORCE_COLOR = os.getenv("FORCE_COLOR", False)


def terminal_supports_colors() -> bool:
    if FORCE_COLOR:
        return True

    if NO_COLOR:
        return False

    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def ansi_escape(*args: int) -> str:
    codes = ";".join((str(a) for a in args))
    return f"\033[{codes}m" if terminal_supports_colors() else ""


ansi_codes: dict[str, int] = {
    "reset": 0,
    "bold": 1,
    "dim": 2,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "inverse": 7,
    "hidden": 8,
    "strikethrough": 9,
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "default": 39,
    "on_black": 40,
    "on_red": 41,
    "on_green": 42,
    "on_yellow": 43,
    "on_blue": 44,
    "on_magenta": 45,
    "on_cyan": 46,
    "on_white": 47,
    "on_default": 49,
}


class Colorize:
    def __init__(self, s: str, /) -> None:
        self._internal = s
        self._codes: list[int] = []

        # i did a lot of magic to avoid boilerplate code...
        # i'm sorry you had to see that... but hey! it works.
        #
        # i'm banking on the fact that this library won't need
        # to be maintained very much since it's pretty standard stuff :)
        for name, code in ansi_codes.items():
            setattr(self, name, self._handler(code))

    def _handler(self, code: int, /) -> Callable[[], Self]:
        def wrapper() -> Self:
            self._codes.append(code)
            return self

        return wrapper

    def __str__(self) -> str:
        # TODO: Instead of resetting at the end, undo the changes.
        # If the user used `bold()`, then write the sequence to reset bold.
        # This way, the user can nest `Colorize`s as they please without
        # one resetting the other. We can probably do a map with the key being
        # the code and the value being the reset code, then just unroll _codes
        # at the end.
        #
        # if code == 38:
        #   if next_code == 5:
        #     skip next value (256-colors code)
        #   else:
        #     skip next 3 values (rgb code)
        #   finally:
        #     reset with 39
        #
        # (do same for bg)
        #
        # check if code is within a range with switch/case pattern matching,
        # if it is, use reset for that range, e.g., 30-40 => 39, 1 => 22
        #
        # For reference:
        # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
        return ansi_escape(*self._codes) + self._internal + ansi_escape(0)

    # TODO: I am in the market for a new name for this function...
    def color256(self, color: int, /) -> Self:
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._codes.extend((38, 5, color))
        return self

    def custom(self, red: int, green: int, blue: int) -> Self:
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._codes.extend((38, 2, red, green, blue))
        return self

    def on_color256(self, color: int, /) -> Self:
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._codes.extend((48, 5, color))
        return self

    def on_custom(self, red: int, green: int, blue: int) -> Self:
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._codes.extend((48, 2, red, green, blue))
        return self

    def __add__(self, other: object) -> str:
        match other:
            case Colorize():
                return str(self) + str(other)
            case str():
                return str(self) + other
            case _:
                raise NotImplementedError

    def __radd__(self, other: object) -> str:
        match other:
            case Colorize():
                return str(other) + str(self)
            case str():
                return other + str(self)
            case _:
                raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        match other:
            case Colorize():
                return str(self) == str(other)
            case str():
                return str(self) == other
            case _:
                raise NotImplementedError

    def __ne__(self, other: object) -> bool:
        match other:
            case Colorize():
                return str(self) != str(other)
            case str():
                return str(self) != other
            case _:
                raise NotImplementedError

    def __iadd__(self, other: object) -> Colorize:
        match other:
            case Colorize():
                self._internal += str(other)
            case str():
                self._internal += other
            case _:
                raise NotImplementedError

        return self
