# wc-tool

A minimal command-line tool for counting file properties, inspired by the Unix `wc` command.

## Requirements

- > = Python 3.13
- Have the `uv` package manager installed

## Setup

1. Clone the GitHub repository
2. Create a virtual environment with uv inside the `wc-tool` folder:

   ```bash
   uv init
   uv venv
   ```

3. Install the `ccwc` using `uv pip install .`
4. (Optional for example testing) Download the test file as mentioned in this [link](https://codingchallenges.fyi/challenges/challenge-wc)

## Usage

`ccwc [OPTIONS]`

### Options

| Flag            | Description          |
| --------------- | -------------------- |
| `-c`, `--bytes` | Print the byte count |
| `-l`, `--lines` | Print the line count |
| `-h`, `--help`  | Show help message    |

## Examples

Count bytes in a file:
`ccwc -c test.txt`

Output:
`342190 test.txt`

## Working Notes

[Working Notes Link](./wc-tool-working-notes.md)
