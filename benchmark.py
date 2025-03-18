import time

from colorize import Colorize

ITERATIONS = 1_000_000


def benchmark(f):
    def wrapper():
        start_time = time.perf_counter()
        result = f()
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"{f.__name__}: {duration:.6f} seconds")
        return result

    return wrapper()


@benchmark
def test_colorize_library():
    for _ in range(ITERATIONS):
        # fmt: off
        _ = (
            Colorize(" What is your name?").bold()
            + Colorize(" Please answer!").color256(213)
        )
        # fmt: on


@benchmark
def test_raw_ansi():
    for _ in range(ITERATIONS):
        # fmt: off
        _ = "\033[1mWhat is your name?\033[22m" + "\033[38;5;213m Please answer!\033[39m"  # noqa: E501
        # fmt: on


# Results:
# Raw string: 0.02s
# Pure Python: 7.3s
# Rust rewrite: 5.9s
# Rust+optimizations: 3.6s
