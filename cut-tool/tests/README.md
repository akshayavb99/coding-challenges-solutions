# Cut Tool Test Suite

Comprehensive test suite for the cut tool implementation.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_field_extraction.py

# Run specific test class
pytest tests/test_field_extraction.py::TestBasicFieldExtraction

# Run specific test
pytest tests/test_field_extraction.py::TestBasicFieldExtraction::test_extract_single_field_tab_delimited

# Run with coverage
pytest --cov=. --cov-report=html
```

## Test Organization

- **test_field_extraction.py**: Core functionality tests
  - Basic field extraction
  - Delimiter handling
  - Edge cases (empty files, out of bounds, etc.)
  - File handling and error cases
  - Output formatting

- **test_cli_arguments.py**: Command-line interface tests
  - Argument parsing
  - Required vs optional arguments
  - Help messages
  - Error handling

## Test Fixtures

Located in `fixtures/`:

- **sample_tab.txt**: Tab-separated data (3 fields, 4 lines)
- **sample_comma.txt**: Comma-separated data
- **sample_pipe.txt**: Pipe-separated data
- **empty.txt**: Empty file
- **single_line.txt**: Single line file
- **with_empty_fields.txt**: File with missing/empty fields

## Coverage Goals

- Field extraction (single and multiple)
- Delimiter variations
- Edge cases (empty files, bounds, duplicates)
- File I/O errors
- CLI argument parsing
- Help and error messages

## Known Issues (As of Current Review)

These tests will initially fail due to bugs in the implementation:

1. Invalid argument validation logic (fields/delimiter check)
2. Exception handling returns exception objects instead of raising
3. Missing -f flag requirement and None handling
4. Incorrect help message usage

These must be fixed before tests pass.
