# Compression Tool

A Python implementation of a Huffman compression and decompression workflow.
The tool reads an input file from the local `data/` directory, writes an encoded
file, decodes it again, and reports the size difference.

## Requirements

- Python 3.13
- `uv` for dependency management

The project dependencies are declared in `pyproject.toml` and locked in
`uv.lock`. The test dependency currently used by the project is `pytest`.

## Setup

From the repository root, move into this project:

```bash
cd compression-tool
```

Install the locked dependencies:

```bash
uv sync --locked
```

If `uv` is not installed, install it first using the official installer for your
platform, then rerun the sync command above.

## Running the Tool

Place the file you want to compress inside the `data/` directory. For example:

```text
compression-tool/
  data/
    test.txt
```

Run the program:

```bash
uv run python main.py
```

When prompted, enter only the filename, not the full path:

```text
Please give the name of the file to be encoded: test.txt
```

The tool creates encoded and decoded output files in the same `data/` directory
and prints the original, encoded, and decoded file sizes.

## Testing

Run the Python test suite from inside `compression-tool`:

```bash
uv run pytest
```

The tests cover Huffman node ordering, tree construction, frequency maps,
prefix tables, metadata handling, encode/decode behavior, and the interactive
CLI workflow.

GitHub Actions also runs these tests whenever files under `compression-tool/`
change.
