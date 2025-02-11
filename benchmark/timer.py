import time

from colorize import Colorize


# Test the library-based approach
def test_colorize_library():
    iterations = 1_000_000
    for _ in range(iterations):
        # Using Colorize (your library)
        # fmt: off
        _ = Colorize(" What is your name?").bold() + Colorize(" Please answer!").color256(213)  # noqa: E501
        # fmt: on


# Test the raw ANSI approach
def test_raw_ansi():
    iterations = 1_000_000
    for _ in range(iterations):
        # Writing raw ANSI escape codes directly
        # fmt: off
        _ = "\033[1mWhat is your name?\033[0m" + "\033[38;5;213m Please answer!\033[0m"  # noqa: E501
        # fmt: on


# Benchmark the Colorize library
start_time = time.perf_counter()
test_colorize_library()
end_time = time.perf_counter()
colorize_duration = end_time - start_time

# Benchmark the raw ANSI approach
start_time = time.perf_counter()
test_raw_ansi()
end_time = time.perf_counter()
raw_ansi_duration = end_time - start_time

# Print results
print(f"Colorize library time: {colorize_duration:.6f} seconds")
print(f"Raw ANSI time: {raw_ansi_duration:.6f} seconds")
# the difference was massive... like... 7.3 seconds vs 0.02 seconds...
# I really like the builder-style chaining approach, so I'm going to try to
# get these numbers a little bit closer.
