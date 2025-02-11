"""
Colorize
========

Use ANSI color codes to color and style the output to your terminal.

Examples
--------

>>> from colorize import Colorize
>>> Colorize("error").bold().red()
"""

from ._colorize import Colorize

__all__ = ("Colorize",)
