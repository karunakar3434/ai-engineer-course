# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Where am I running? Interpreter, environment and import path.

Run it two ways and compare:
    uv run lessons/week-01/examples/01_where_am_i.py
    cd playground/hello-uv && uv run python ../../lessons/week-01/examples/01_where_am_i.py
"""

import sys
import sysconfig


def main() -> None:
    print(f"Python version : {sys.version.split()[0]}")
    print(f"Interpreter    : {sys.executable}")
    print(f"Environment    : {sys.prefix}")
    print(f"Base install   : {sys.base_prefix}")
    print(f"In a venv?     : {sys.prefix != sys.base_prefix}")
    print(f"site-packages  : {sysconfig.get_path('purelib')}")
    print("\nsys.path (searched in order, like a classpath):")
    for i, entry in enumerate(sys.path):
        print(f"  [{i}] {entry or '(current directory)'}")


if __name__ == "__main__":
    main()
