from typing import Callable

def interface_repeater(func: Callable) -> Callable:
    """Supporting decorator. It allows repeat command request if enter invalid value."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                raise KeyboardInterrupt("It's time to close!")
            except ValueError:
                print("\nIncorrect input! Try again.")
    return wrapper