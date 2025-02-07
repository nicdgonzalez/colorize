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

print(Colorize(" 1 ").on_cyan() + Colorize(" What is your name?").bold())
name = input("> ")
print()

print("Hi", Colorize(name).bold().color256(213) + "!")
print()

while 1:
    print(Colorize("Woah... we are stuck inside a loop!").color256(220))
    print(Colorize("Press CTRL+C to break the loop!").color256(0).on_green())

    try:
        _ = input()
    except KeyboardInterrupt:
        break
print()

print(Colorize("All done! I hope you find this project useful!").italic())
```
