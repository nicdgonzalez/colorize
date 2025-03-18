# Colorize

**Colorize** allows you to apply ANSI color codes for styling text in the
terminal effortlessly, using a clean, builder-style method chaining approach.

## Installation

**Requires Python 3.10 or higher.**

This project is not on PyPI, but you can still install it using pip:

```bash
pip install git+https://github.com/nicdgonzalez/colorize.git
```

### Quickstart

Here is a simple example to help get you started:

```py
from colorize import Colorize

print(Colorize(" 1 ").on_cyan() + Colorize(" What is your name?").bold())
name = input("> ")
print()

print("Hi", Colorize(name).bold().green() + "!")
print()

while 1:
    print(Colorize("Woah... we are stuck inside a loop!").color256(220))
    print(Colorize("Press CTRL+C to break the loop!").black().on_red())

    try:
        _ = input()
    except KeyboardInterrupt:
        break
print()

print(Colorize("All done! I hope you find this project useful!").italic())
```

For an example of this library in action, see [nicdgonzalez/status](../status).

## Performance

While I haven't conducted a direct comparison of this library with others that
serve a similar purpose, the primary goal of this library is to provide a more
ergonomic and intuitive way to add color to the terminal. Nevertheless, I have
made every effort to optimize its performance. If you're interested, see
[`benchmark.py`](./benchmark.py).
