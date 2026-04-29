# Working Document - Build your own `wc` tool

File structure generated with the help of CLAUDE chat

**John Crickett's Coding Challenges**

---

## 1. Challenge Overview

| Field                 | Details                                                             |
| --------------------- | ------------------------------------------------------------------- |
| **Challenge Name**    | Build Your Own `wc` Tool                                            |
| **Challenge #**       | #1                                                                  |
| **Source**            | [Coding Challenges by John Crickett](https://codingchallenges.fyi/) |
| **Language**          | Python                                                              |
| **Runtime / Version** | Python 3.13                                                         |
| **Date Started**      | 2026-04-27                                                          |
| **Target Completion** | 2026-05-03                                                          |
| **Status**            | `In Progress`                                                       |

---

## 2. Problem Statement

> Requirement is to build my version of the `wc` tool which is found in Unix and Linux. It must be able to replicate the functionalities of the
> actual `wc` tool.

- **Inputs:** The contents of the file to be processed OR standard input
- **Outputs:** Based on the option provided, for the given file, the tool should return
  - Number of bytes
  - Number of characters
  - Number of words
  - Number of newlines

---

## 3. Initial Thoughts

- **First approach considered:**
  - For all steps from 1 to 6, standard approach would be to read the file into a very long string and then do the count checks as per provided options, but this runs the risk of Out-Of-Memory (OOM) if the file is too large (Not sure about the limit - need to test it)
  - Possible approach - read in streaming or chunks, and read in binary format (binary format is needed to count the number of bytes)
  - Two ways to implement the counts - each count as its own function or all the counts in the single function
- **What's confusing or unclear:**
  - Whether to prioritize correctness vs performance for large files (especially for word/character counting).
  - Exact definition differences between bytes, characters, and words in edge cases (Unicode, multiple spaces, newlines).
  - Whether to support stdin early or only after file-based implementation.
- **Wrong paths you anticipated or tried:**
  - Initially considering loading entire file into memory as a string for simplicity.
  - Realized this could fail for very large files (OOM risk), so shifted toward streaming/chunk-based processing

---

## 4. Goals & Success Criteria

### Goals

- Understand the core mechanics behind `wc`
- Practice file parsing, standard input parsing
- Produce a working CLI tool that mirrors real-world behavior for the required functionalities

### Success Criteria

- [x] All required steps from the challenge pass
- [x] Output matches the reference tool on test inputs

---

## 5. Scope

### In Scope

For every input file or standard input, count and return the following:

- Number of bytes
- Number of characters
- Number of words
- Number of lines

### Out of Scope

- Performance optimization beyond functional correctness
- GUI or web interface
- The `max-line-length` functionality in the original `wc` tool
- Handling multiple file inputs
- Error handling logic

---

## 6. Functional Requirements

In the upcoming steps, the sample file `test.txt` is provided as part of the challenge description.

### Step 0

- **Description:** Basic setup. Read through the `man` page for `wc` and choose the programming language.

### Step 1

- **Description:** Write a simple version of the `wc` tool which takes the command option `-c` and outputs the number of bytes in a file.
- **Acceptance Criteria:** Consider the tool name to be `ccwc`
  - Input: `ccwc -c test.txt`
  - Expected Output: `342190 test.txt`

### Step 2

- **Description:** Write a simple version of the `wc` tool which takes the command option `-l` that outputs the number of lines in a file.
- **Acceptance Criteria:**
  - Input: `ccwc -l test.txt`
  - Expected Output: `7145 test.txt`

### Step 3

- **Description:** Write a simple version of the `wc` tool which takes the command option `-w` that outputs the number of words in a file.
- **Acceptance Criteria:**
  - Input: `ccwc -w test.txt`
  - Expected Output: `58164 test.txt`

### Step 4

- **Description:** Write a simple version of the `wc` tool which takes the command option `-m` that outputs the number of characters in a file.
- **Acceptance Criteria:**
  - Input: `ccwc -m test.txt`
  - Expected Output: `339292 test.txt`

### Step 5

- **Description:** Write a simple version of the `wc` tool which takes the default option - i.e. no options are provided, which is the equivalent to the `-c`, `-l` and `-w` options.
- **Acceptance Criteria:**
  - Input: `ccwc test.txt`
  - Expected Output: `7145   58164  342190 test.txt`

### Step 6

- **Description:** Write a simple version of the `wc` tool to support being able to read from standard input if no filename is specified.
- **Acceptance Criteria:**
  - Input: `cat test.txt | ccwc -l`
  - Expected Output: `7145`

---

## 7. Technical Design

### Architecture / Approach

```
main.py       — Entry point, argument parsing, File / stdin reading logic, Primary processing logic, Output formatting
```

### Algorithm / Logic Notes

- Count bytes using raw byte length, not character count, to match `wc -c` behavior

### Non-Functional Requirements

| Requirement      | Detail                                       |
| ---------------- | -------------------------------------------- |
| **Dependencies** | stdlib only                                  |
| **Platform**     | cross-platform                               |
| **Performance**  | Handle small to large files without crashing |

---

## 8. Implementation

### v1 — Working Solution

- **Approach:** It processes files using binary mode + streaming reads to efficiently handle large files without loading everything into memory. Each metric is implemented as a separate function:
  - Bytes - uses file pointer position (seek + tell)
  - Lines - counts newline bytes in chunks
  - Words - tracks transitions between whitespace and non-whitespace bytes
  - Characters - decodes UTF-8 safely and counts resulting characters
- **Key decisions made:**
  - Used binary file reading (rb) for consistency across all metrics.
  - Used chunk-based reading (8KB or 8192 bytes) to support large files efficiently.
  - Implemented word counting using state tracking (in_word) instead of splitting strings.
  - Used argparse for CLI flag handling similar to real Unix tools.

```
# v1 sample solution

#!/usr/bin/env python3

import argparse # Needed to receive and process the input arguments

def count_bytes(filepath):
    """
     Count the number of bytes in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total size of the file in bytes.
     """
    with open(filepath, "rb") as f:
        f.seek(0, 2)   # move to end
        return f.tell()  # byte position = size

def count_lines(filepath, chunk_size=8192):
    """
     Count the number of lines in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total number of lines.
     """
    count = 0
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            count += chunk.count(b"\n")
    return count

def count_words(filepath, chunk_size=8192):
    """
     Count the number of words in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total number of words.
     """
    WHITESPACE = set(b" \t\n\r\v\f")
    in_word = False
    count = 0

    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            for byte in chunk:
                if byte in WHITESPACE:
                    in_word = False
                else:
                    if not in_word:
                        count += 1
                        in_word = True

    return count

def count_characters(filepath, chunk_size=8192):
    """
     Count the number of characters in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total number of characters (Unicode code points).
     """
    count = 0

    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            count += len(chunk.decode("utf-8", errors="replace"))

    return count

def main():
    """
     Entry point for the wc-tool CLI.

     Parses command-line arguments and dispatches to the appropriate
     counting function. Prints results to stdout.
     """
    # Define argument parser
    parser = argparse.ArgumentParser(description="Hello from wc-tool!")

    # Add flags
    parser.add_argument("-c", "--bytes", action="store_true", help="Count bytes")
    parser.add_argument("-l", "--lines", action="store_true", help="Count number of lines")
    parser.add_argument("-w", "--words", action="store_true", help="Count number of words")
    parser.add_argument("-m", "--characters", action="store_true", help="Count number of characters")

    # Add argument for taking filename as input
    parser.add_argument("file", help="File to process")

    # Parse the arguments
    args = parser.parse_args()

    # Get the required results
    result = []
    if not any([args.bytes, args.lines, args.words, args.characters]):
        size = count_bytes(args.file)
        line_count = count_lines(args.file)
        word_count = count_words(args.file)

        result.append(str(line_count))
        result.append(str(word_count))
        result.append(str(size))

    else:

        if args.bytes:
            size = count_bytes(args.file)
            result.append(str(size))
            #print(f"{size} {args.file}")

        if args.lines:
            line_count = count_lines(args.file)
            result.append(str(line_count))
            #print(f"{line_count} {args.file}")

        if args.words:
            word_count = count_words(args.file)
            result.append(str(word_count))
            #print(f"{word_count} {args.file}")

        if args.characters:
            char_count = count_characters(args.file)
            result.append(str(char_count))
            #print(f"{char_count} {args.file}")

    print(" ".join(result) + " " + args.file)

# Entry point
if __name__ == "__main__":
    main()

```

### Refactoring Notes

The refactor significantly changes the structure from a collection of independent counting functions into a pipeline-based streaming structure.

1. Introduced shared state object

- Replaced separate counters with a single Counters class.
- Centralized all metrics (lines, words, bytes, chars) and word-state tracking (in_word).
- Impact: Cleaner state management and easier extensibility.

2. Moved to a pipeline-based design

- Replaced standalone counting functions with handler functions:
- handle_bytes, handle_lines, handle_words, handle_chars
- Each handler updates shared state per chunk.
- Impact: Modular design where features can be enabled/disabled dynamically.

3. Added stream processing engine

- Introduced process_stream() as the core loop.
- Handles chunk reading and delegates work to handlers.
- Impact: Centralized I/O logic and eliminated duplication.

4. Dynamic handler selection

- Built handler list based on CLI flags (or default mode).
- Default behavior mimics wc (-l -w -c).
- Impact: Cleaner CLI logic and flexible configuration.

5. Improved separation of concerns

- Clear split between CLI parsing (main), Processing engine (process_stream), Computation (handlers), State (Counters)
- Impact: Easier to maintain and extend.

```
# refactored version here
Refer to ./main.py
```

---

## 9. Additional Test Plan

| Test Case                        | Input                     | Expected Output                                 |
| -------------------------------- | ------------------------- | ----------------------------------------------- |
| Basic file                       | `ccwc test.txt`           | `7145 58164 342190 test.txt`                    |
| Empty file                       | `ccwc empty.txt`          | `0 0 0 empty.txt`                               |
| No arguments (default mode)      | `ccwc test.txt`           | `7145 58164 342190 test.txt`                    |
| Line count only                  | `ccwc -l test.txt`        | `7145`                                          |
| Word count only                  | `ccwc -w test.txt`        | `58164`                                         |
| Byte count only                  | `ccwc -c test.txt`        | `342190`                                        |
| Character count only             | `ccwc -m test.txt`        | `339292`                                        |
| Multiple flags                   | `ccwc -l -w test.txt`     | `7145 58164 test.txt`                           |
| Combined flags (order variation) | `ccwc -wl test.txt`       | `7145 58164 test.txt`                           |
| File with no trailing newline    | `ccwc no_newline.txt`     | Correct counts, e.g. `10 20 100 no_newline.txt` |
| Stdin input (line count)         | `cat test.txt \| ccwc -l` | `7145`                                          |
| Stdin default mode               | `cat test.txt \| ccwc`    | `7145 58164 342190`                             |

---

## 10. Performance & Complexity

### Time Complexity

- Best case: O(n) — single pass over input stream
- Worst case: O(n) — every byte processed once

### Space Complexity

- Analysis: O(1) additional memory (excluding input stream buffer). Fixed-size state object regardless of file size

### Scaling Thoughts

- What happens with very large inputs?: Handles large files efficiently since the data is processed in chunks from files. However, for standard input, the entire input is first stored
- Potential bottlenecks: UTF-8 decoding in character counting
- Possible improvements: Handling multiple files in a single input

---

## 11. Real-World Considerations

- **Error handling:** Currently minimal; assumes file exists and is readable. In production, should handle:
  - FileNotFoundError
  - Permission errors
  - Invalid encoding issues (especially for character counting)
- **Input validation:**
  - No validation for conflicting flags (e.g., multiple redundant combinations).
  - Assumes valid UTF-8-compatible file input for character counting.
- **Logging / observability:**
  - No logging implemented (typical for CLI utility at this stage).
  - Could add debug logging for chunk processing in large file scenarios.

---

## 12. References & Resources

- **Challenge URL:** `https://codingchallenges.fyi/challenges/challenge-wc`
- **References:**
  - `man wc`
  - https://realpython.com/read-write-files-python
  - https://realpython.com/working-with-files-in-python/

---

## 13. Progress Log

| Date       | Time Spent | Notes                                                                                                                                            |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-04-27 | 1h 0m      | Started Step 0 — Basic setup, filled initial information in PRD                                                                                  |
| 2026-04-28 | 1h 15m     | Completed Step 1 (Count number of bytes) and Step 2 (Count number of lines), along with `uv` based tool setup steps and initial README           |
| 2026-04-28 | 2h 0m      | Completed Step 3 (Count number of words), Step 4 (Count number of characters), and Step 5 (Handle case where no flags are passed)                |
| 2026-04-29 | 2h 20m     | Completed Step 5 (Count number of words), Step 6 (Count number of characters), refactoring the initial version to a more pipeline-based approach |

**Total Time:** ~7 hours

---

## 14. Retrospective

## **What went well?**

- Deciding the chunk-based approach made the later refactoring easier
- Refactoring to determine the list of count calculations needed helped avoid multiple reads of the same file
- The shared state through the `Counters` class made it easy to have all the counts in one easily accessible and understandable place

## **What was harder than expected?**

- Implementing word counting correctly in a streaming context required careful handling of state across chunk boundaries
- Refactoring from individual functions that each read the file to functions that simply process a given chunk at a time
- Refactoring to store the list of functions was something I had to search and think more about

## **What did I learn?**

- How real-world tools avoid OOM issues using streaming and chunk-based processing instead of loading entire files into memory
- Understanding the difference in implementation for counting bytes vs counting characters
- Storing functions as a list of callables
- Handling stdin input instead of reading from files

## **What would I do differently next time?**

- Defining more edge cases
- Better testing strategy with pytest for example
