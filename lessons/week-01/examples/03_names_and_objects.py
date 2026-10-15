# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Names, references and identity: the Java reference model, applied to everything.

Run one part at a time so you can predict first:
    uv run lessons/week-01/examples/03_names_and_objects.py aliasing
Parts: aliasing, augmented, args, identity (no argument runs them all).
"""

import sys


def aliasing() -> None:
    # A service keeps its default retry config, and a request handler "copies" it.
    default_retries = [1, 2, 4]
    request_retries = default_retries  # no copy: a second name for the same list
    request_retries.append(8)
    print("default_retries:", default_retries)
    print("same object?    ", request_retries is default_retries)
    print("id() of each:   ", id(default_retries), id(request_retries))

    safe_copy = list(default_retries)  # or default_retries.copy() or default_retries[:]
    safe_copy.append(16)
    print("after copying:  ", default_retries, "vs", safe_copy)


def augmented() -> None:
    # `+=` on a list mutates in place; `x = x + ...` builds a new list and rebinds the name.
    a = [1, 2]
    b = a
    b += [3]
    print("b += [3]     ->  a =", a, "| a is b:", a is b)

    a = [1, 2]
    b = a
    b = b + [3]  # noqa: RUF005 (the demo: concatenation builds a new list)
    print("b = b + [3]  ->  a =", a, "| a is b:", a is b)

    # Immutable types can't change in place, so `+=` always rebinds.
    s = "GET"
    t = s
    t += " /health"
    print("str +=       ->  s =", repr(s), "| s is t:", s is t)


def add_tag(tags: list[str], tag: str) -> None:
    tags.append(tag)  # mutates the caller's list


def replace_tags(tags: list[str], tag: str) -> None:
    tags = [tag]  # noqa: F841 (ruff spots it too: this rebinding is never seen)


def args() -> None:
    tags = ["prod"]
    add_tag(tags, "eu-west")
    print("after add_tag:     ", tags)
    replace_tags(tags, "staging")
    print("after replace_tags:", tags)


def identity() -> None:
    a = [1, 2]
    b = [1, 2]
    print("[1, 2] == [1, 2]:", a == b, "| is:", a is b)

    # CPython caches the ints -5..256 (Java's Integer cache is -128..127).
    # int(...) at runtime avoids the compiler sharing one constant for both sides.
    print("int('256') is int('256'):", int("256") is int("256"))
    print("int('257') is int('257'):", int("257") is int("257"))
    print("int('257') == int('257'):", int("257") == int("257"))

    result = None
    print("result is None:", result is None)  # the one everyday use of `is`


PARTS = {"aliasing": aliasing, "augmented": augmented, "args": args, "identity": identity}

if __name__ == "__main__":
    chosen = sys.argv[1:] or list(PARTS)
    for name in chosen:
        print(f"--- {name} ---")
        PARTS[name]()
