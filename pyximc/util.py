from os.path import abspath, dirname, join
from typing import Callable

def initialise(file: str) -> None:
    """
    Initialises the libximc library. If the library is not found among the pip installed packages,
    it tries to import the library using relative path: ../../../ximc/crossplatform/wrappers/python.
    """
    try:
        import libximc.highlevel as ximc
        print(f"Use libximc {ximc.ximc_version()} that has been found among the pip installed packages")
    except ImportError:
        print("Warning! libximc cannot be found among the pip installed packages. Did you forget to install it via pip?\n"
            "Trying to import the library using relative path: ../../../ximc/crossplatform/wrappers/python ...")
        import sys
        cur_dir = abspath(dirname(file))
        ximc_dir = join(cur_dir, "..", "..", "..", "ximc")
        ximc_package_dir = join(ximc_dir, "crossplatform", "wrappers", "python")
        sys.path.append(ximc_package_dir)
        import libximc.highlevel as ximc
        print("Initialisation Success!")


def interface_repeater(func: Callable) -> Callable:
    """Supporting decorator. It allows repeat command request if enter invalid value."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                raise KeyboardInterrupt("It's time to close!")
            except Exception:
                print("\nIncorrect input! Try again.")
    return wrapper