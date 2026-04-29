#!/usr/bin/env python3

"""
ccwc - Pipeline-based wc implementation.
"""

import argparse
import sys


# ============================================================
# Shared state container
# ============================================================
class Counters:
    """Holds all counting state."""
    def __init__(self):
        self.lines = 0
        self.words = 0
        self.bytes = 0
        self.chars = 0
        self.in_word = False


# ============================================================
# Handlers (pipeline functions)
# ============================================================

WHITESPACE = b" \t\n\r\v\f"


def handle_bytes(state, chunk):
    """Count raw bytes."""
    state.bytes += len(chunk)


def handle_lines(state, chunk):
    """Count newline characters."""
    state.lines += chunk.count(b"\n")


def handle_words(state, chunk):
    """Count words using whitespace transitions."""
    for b in chunk:
        if b in WHITESPACE:
            state.in_word = False
        else:
            if not state.in_word:
                state.words += 1
                state.in_word = True


def handle_chars(state, chunk):
    """Count Unicode characters (decoded)."""
    state.chars += len(chunk.decode("utf-8", errors="replace"))


# ============================================================
# Stream processor (pipeline engine)
# ============================================================
def process_stream(f, handlers, chunk_size=8192):
    """
    Run a single-pass pipeline over a stream.

    Args:
        f: binary stream (file or stdin)
        handlers: list of functions(state, chunk)
        chunk_size: read size

    Returns:
        Counters object with results
    """

    state = Counters()

    while chunk := f.read(chunk_size):
        for handler in handlers:
            handler(state, chunk)

    return state

def main():
    parser = argparse.ArgumentParser(description="wc-tool (ccwc) - Python-based wc implementation")

    parser.add_argument("-c", "--bytes", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    parser.add_argument("-m", "--characters", action="store_true")

    parser.add_argument("file", nargs="?", default=None)

    args = parser.parse_args()

    # Input source
    f = open(args.file, "rb") if args.file else sys.stdin.buffer

    with f:
        handlers = []

        default = not any([args.bytes, args.lines, args.words, args.characters])

        if args.bytes or default:
            handlers.append(handle_bytes)

        if args.lines or default:
            handlers.append(handle_lines)

        if args.words or default:
            handlers.append(handle_words)

        if args.characters:
            handlers.append(handle_chars)
            
        state = process_stream(f, handlers)

    # --------------------------------------------------------
    # Output formatting
    # --------------------------------------------------------
    result = []

    if default:
        result = [str(state.lines), str(state.words), str(state.bytes)]
    else:
        if args.lines:
            result.append(str(state.lines))
        if args.words:
            result.append(str(state.words))
        if args.bytes:
            result.append(str(state.bytes))
        if args.characters:
            result.append(str(state.chars))

    suffix = f" {args.file}" if args.file else ""
    print(" ".join(result) + suffix)


if __name__ == "__main__":
    main()