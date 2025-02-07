# Colorize

Use ANSI color codes to color/style text in the terminal.

## Getting started

This project is not on PyPI, but you can still use `pip` to install it:

```bash
pip install --depth=1 git+https://github.com/nicdgonzalez/colorize.git
```

Here is a simple example to help get you started:

```python
from colorize import Colorize

print(Colorize("1").bold().cyan(), "What is your name?")
name = input("> ")

print("Hello,", Colorize(name).bold().color256(219) + "!")

print(Colorize("Press CTRL+C to break the loop!").color256(255).on_cyan())
while 1:
    try:
        _ = input()
    except KeyboardInterrupt:
        break

print("Hello,", Colorize("World").italic() + "!")
```
