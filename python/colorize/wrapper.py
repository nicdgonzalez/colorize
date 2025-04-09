from colorize._colorize import _Colorize


class Colorize:
    def __init__(self, s: str, /) -> None:
        self._internal = _Colorize(s)

    def __str__(self) -> str:
        return str(self._internal)

    def bold(self) -> "Colorize":
        self._internal.bold()
        return self

    def dim(self) -> "Colorize":
        self._internal.dim()
        return self

    def italic(self) -> "Colorize":
        self._internal.italic()
        return self

    def underline(self) -> "Colorize":
        self._internal.underline()
        return self

    def blink(self) -> "Colorize":
        self._internal.blink()
        return self

    def inverse(self) -> "Colorize":
        self._internal.inverse()
        return self

    def hidden(self) -> "Colorize":
        self._internal.hidden()
        return self

    def strikethrough(self) -> "Colorize":
        self._internal.strikethrough()
        return self

    def black(self) -> "Colorize":
        self._internal.black()
        return self

    def red(self) -> "Colorize":
        self._internal.red()
        return self

    def green(self) -> "Colorize":
        self._internal.green()
        return self

    def yellow(self) -> "Colorize":
        self._internal.yellow()
        return self

    def blue(self) -> "Colorize":
        self._internal.blue()
        return self

    def magenta(self) -> "Colorize":
        self._internal.magenta()
        return self

    def cyan(self) -> "Colorize":
        self._internal.cyan()
        return self

    def white(self) -> "Colorize":
        self._internal.white()
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
            The class itself to allow for builder-style method chaining.
        """
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._internal.color256(color)

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
            The class itself to allow for builder-style method chaining.
        """
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._internal.true_color(red, green, blue)

        return self

    def on_black(self) -> "Colorize":
        self._internal.on_black()
        return self

    def on_red(self) -> "Colorize":
        self._internal.on_red()
        return self

    def on_green(self) -> "Colorize":
        self._internal.on_green()
        return self

    def on_yellow(self) -> "Colorize":
        self._internal.on_yellow()
        return self

    def on_blue(self) -> "Colorize":
        self._internal.on_blue()
        return self

    def on_magenta(self) -> "Colorize":
        self._internal.on_magenta()
        return self

    def on_cyan(self) -> "Colorize":
        self._internal.on_cyan()
        return self

    def on_white(self) -> "Colorize":
        self._internal.on_white()
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
            The class itself to allow for builder-style method chaining.
        """
        if 0 > color > 255:
            raise ValueError("color must be between 0 and 255, inclusive")

        self._internal.on_color256(color)

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
            The class itself to allow for builder-style method chaining.
        """
        colors = (red, green, blue)

        if any((0 > color > 255 for color in colors)):
            raise ValueError("all values must be between 0 and 255, inclusive")

        self._internal.on_true_color(red, green, blue)

        return self

    def __add__(self, other: object) -> str:
        match other:
            case Colorize():
                return str(self) + str(other)
            case str():
                return str(self) + other
            case _:
                return NotImplemented

    def __radd__(self, other: object) -> str:
        match other:
            case Colorize():
                return str(other) + str(self)
            case str():
                return other + str(self)
            case _:
                return NotImplemented

    def __eq__(self, other: object) -> bool:
        match other:
            case Colorize():
                return str(self) == str(other)
            case str():
                return str(self) == other
            case _:
                return NotImplemented

    def __ne__(self, other: object) -> bool:
        match other:
            case Colorize():
                return str(self) != str(other)
            case str():
                return str(self) != other
            case _:
                return NotImplemented

    def __iadd__(self, other: object) -> "Colorize":
        return NotImplemented
