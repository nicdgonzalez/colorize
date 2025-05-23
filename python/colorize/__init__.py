"""
Colorize
========

**Colorize** allows you to apply ANSI color codes for styling text in the
terminal effortlessly, using a clean, builder-style method chaining approach.

Example
-------
>>> from colorize import Colorize
>>>
>>> print(Colorize(" 1 ").on_cyan() + Colorize(" What is your name?").bold())
>>> name = input("> ")
>>> print()
>>>
>>> print("Hi", Colorize(name).bold().green() + "!")
>>> print()
>>>
>>> while 1:
...     print(Colorize("Woah... we are stuck inside a loop!").color256(220))
...     print(Colorize("Press CTRL+C to break the loop!").black().on_red())
...
...     try:
...         _ = input()
...     except KeyboardInterrupt:
...         break
>>> print()
>>>
>>> print(Colorize("All done! I hope you find this project useful!").italic())
"""

from .wrapper import Colorize

__all__ = ("Colorize",)
