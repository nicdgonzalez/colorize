import enum
import os
import sys

NO_COLOR = os.getenv("NO_COLOR", False)
FORCE_COLOR = os.getenv("FORCE_COLOR", False)


class Style(enum.IntEnum):
    RESET_ALL = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    INVERSE = 7
    HIDDEN = 8
    STRIKETHROUGH = 9
    RESET_BOLD = 22
    RESET_ITALIC = 23
    RESET_UNDERLINE = 24
    RESET_BLINK = 25
    RESET_INVERSE = 27
    RESET_HIDDEN = 28
    RESET_STRIKETHROUGH = 29


class Foreground(enum.IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    CUSTOM = 38
    DEFAULT = 39


class Background(enum.IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    CUSTOM = 48
    DEFAULT = 49


def terminal_supports_colors() -> bool:
    """Check whether the current terminal supports ANSI color codes"""
    if FORCE_COLOR:
        return True

    if NO_COLOR:
        return False

    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def ansi_escape(*args: int) -> str:
    """Convert a set of codes into a chain of ANSI escape sequences"""
    codes = ";".join((str(a) for a in args))
    return f"\033[{codes}m" if terminal_supports_colors() else ""


class Colorize:
    """Wraps a string to add color-related functionality"""

    def __init__(self, s: str, /) -> None:
        self._internal = s
        self._codes: list[int] = []

    def __str__(self) -> str:
        if len(self._codes) < 1:
            return self._internal

        reset = []
        i = 0

        while i < len(self._codes):
            code = self._codes[i]
            reset_code = self.get_reset_code(code)
            reset.append(reset_code)

            # For codes that are a combination of values, we only need
            # the first value. Increment `i` so it skips over the remainder.
            if code == 38 or code == 48:
                next_code = self._codes[i + 1]

                if next_code == 5:
                    i += 1 + 1  # Skip 5 and the 8-bit color value.
                elif next_code == 2:
                    i += 1 + 3  # Skip 2 and the three RGB color values.
                else:
                    raise AssertionError("unreachable")

            i += 1

        ret = ansi_escape(*self._codes) + self._internal + ansi_escape(*reset)
        self._codes.clear()
        return ret

    @staticmethod
    def get_reset_code(code: int, /) -> int | None:
        match code:
            case Style.BOLD | Style.DIM:
                return Style.RESET_BOLD
            case Style.ITALIC:
                return Style.RESET_ITALIC
            case Style.UNDERLINE:
                return Style.RESET_UNDERLINE
            case Style.BLINK:
                return Style.RESET_BLINK
            case Style.INVERSE:
                return Style.RESET_INVERSE
            case Style.HIDDEN:
                return Style.RESET_HIDDEN
            case Style.STRIKETHROUGH:
                return Style.RESET_STRIKETHROUGH
            case (
                Foreground.BLACK
                | Foreground.RED
                | Foreground.GREEN
                | Foreground.YELLOW
                | Foreground.BLUE
                | Foreground.MAGENTA
                | Foreground.CYAN
                | Foreground.WHITE
                | Foreground.CUSTOM
            ):
                return Foreground.DEFAULT
            case (
                Background.BLACK
                | Background.RED
                | Background.GREEN
                | Background.YELLOW
                | Background.BLUE
                | Background.MAGENTA
                | Background.CYAN
                | Background.WHITE
                | Background.CUSTOM
            ):
                return Background.DEFAULT
            case (
                Style.RESET_ALL
                | Style.RESET_BOLD
                | Style.RESET_UNDERLINE
                | Style.RESET_BLINK
                | Style.RESET_INVERSE
                | Style.RESET_HIDDEN
                | Style.RESET_STRIKETHROUGH
                | Foreground.DEFAULT
                | Background.DEFAULT
            ):
                # Reset codes are part of the magic that happens for you.
                # Since I don't provide methods to add these in, this line
                # should be unreachable.
                raise AssertionError("unreachable")
            case _:
                raise ValueError("invalid code")

    def bold(self) -> "Colorize":
        self._codes.append(Style.BOLD)
        return self

    def dim(self) -> "Colorize":
        self._codes.append(Style.DIM)
        return self

    def italic(self) -> "Colorize":
        self._codes.append(Style.ITALIC)
        return self

    def underline(self) -> "Colorize":
        self._codes.append(Style.UNDERLINE)
        return self

    def blink(self) -> "Colorize":
        self._codes.append(Style.BLINK)
        return self

    def inverse(self) -> "Colorize":
        self._codes.append(Style.INVERSE)
        return self

    def hidden(self) -> "Colorize":
        self._codes.append(Style.HIDDEN)
        return self

    def strikethrough(self) -> "Colorize":
        self._codes.append(Style.STRIKETHROUGH)
        return self

    def black(self) -> "Colorize":
        self._codes.append(Foreground.BLACK)
        return self

    def red(self) -> "Colorize":
        self._codes.append(Foreground.RED)
        return self

    def green(self) -> "Colorize":
        self._codes.append(Foreground.GREEN)
        return self

    def yellow(self) -> "Colorize":
        self._codes.append(Foreground.YELLOW)
        return self

    def blue(self) -> "Colorize":
        self._codes.append(Foreground.BLUE)
        return self

    def magenta(self) -> "Colorize":
        self._codes.append(Foreground.MAGENTA)
        return self

    def cyan(self) -> "Colorize":
        self._codes.append(Foreground.CYAN)
        return self

    def white(self) -> "Colorize":
        self._codes.append(Foreground.WHITE)
        return self

    def color256(self, color: int, /) -> "Colorize":
        """An 8-bit color.

        Parameters
        ----------
        color: int
            A value between 0 and 255, inclusive.

        Errors
        ------
        ValueError:
            If `color` is not between 0 and 255, inclusive.

        Returns
        -------
        Colorize:
            An instance of the class itself to allow for builder-style method
            chaining.
        """
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._codes.extend((Foreground.CUSTOM, 5, color))

        return self

    def true_color(self, red: int, green: int, blue: int) -> "Colorize":
        """A 24-bit color.

        Parameters
        ----------
        red: int
            A value between 0 and 255, inclusive.
        green: int
            A value between 0 and 255, inclusive.
        blue: int
            A value between 0 and 255, inclusive.

        Errors
        ------
        ValueError:
            If any of the values are not between 0 and 255, inclusive.

        Returns
        -------
        Colorize:
            An instance of the class itself to allow for builder-style method
            chaining.
        """
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._codes.extend((Foreground.CUSTOM, 2, red, green, blue))

        return self

    def on_black(self) -> "Colorize":
        self._codes.append(Background.BLACK)
        return self

    def on_red(self) -> "Colorize":
        self._codes.append(Background.RED)
        return self

    def on_green(self) -> "Colorize":
        self._codes.append(Background.GREEN)
        return self

    def on_yellow(self) -> "Colorize":
        self._codes.append(Background.YELLOW)
        return self

    def on_blue(self) -> "Colorize":
        self._codes.append(Background.BLUE)
        return self

    def on_magenta(self) -> "Colorize":
        self._codes.append(Background.MAGENTA)
        return self

    def on_cyan(self) -> "Colorize":
        self._codes.append(Background.CYAN)
        return self

    def on_white(self) -> "Colorize":
        self._codes.append(Background.WHITE)
        return self

    def on_color256(self, color: int, /) -> "Colorize":
        """An 8-bit color.

        Parameters
        ----------
        color: int
            A value between 0 and 255, inclusive.

        Errors
        ------
        ValueError:
            If `color` is not between 0 and 255, inclusive.

        Returns
        -------
        Colorize:
            An instance of the class itself to allow for builder-style method
            chaining.
        """
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._codes.extend((Background.CUSTOM, 5, color))

        return self

    def on_true_color(self, red: int, green: int, blue: int) -> "Colorize":
        """A 24-bit color.

        Parameters
        ----------
        red: int
            A value between 0 and 255, inclusive.
        green: int
            A value between 0 and 255, inclusive.
        blue: int
            A value between 0 and 255, inclusive.

        Errors
        ------
        ValueError:
            If any of the values are not between 0 and 255, inclusive.

        Returns
        -------
        Colorize:
            An instance of the class itself to allow for builder-style method
            chaining.
        """
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._codes.extend((Background.CUSTOM, 2, red, green, blue))

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

    def __iadd__(self, other: object) -> "Colorize":
        match other:
            case Colorize():
                self._internal += str(other)
            case str():
                self._internal += other
            case _:
                raise NotImplementedError

        return self
