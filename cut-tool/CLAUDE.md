# cut-tool/CLAUDE.md

# Challenge: Build Your Own cut Tool

These instructions apply only within cut-tool/.

The goal is to implement a Unix-style cut utility.

## Review Focus

Evaluate behavior against real cut semantics.

Review:

- field selection
- delimiter handling
- range parsing
- stdin support
- file input
- output formatting
- error handling

## High-Risk Areas

### Range Parsing

Review:

- single fields
- ranges
- overlapping ranges
- duplicate ranges
- open-ended ranges
- invalid ranges
- descending ranges

Examples:

1
1-3
2-
-5
1,3,5
1-3,7-9

### Delimiter Handling

Review:

- missing delimiters
- repeated delimiters
- empty fields
- trailing delimiters

### Input Sources

Review:

- stdin
- files
- multiple files
- empty files
- files without trailing newline

### UTF-8

If implementing byte mode:

- verify behavior with multibyte characters
- add tests documenting expected behavior

## Required Test Coverage

Must include tests for:

- field extraction
- multiple field selection
- range selection
- malformed ranges
- empty input
- stdin processing
- file processing
- delimiter edge cases
- output ordering
- duplicate selections

## Review Report Location

Store review reports in:

docs/reviews/

Create a new review file for every review.

Never overwrite prior reports.

## Merge Standard

Behavior must match challenge requirements.

If correctness is uncertain:

Request Changes.
