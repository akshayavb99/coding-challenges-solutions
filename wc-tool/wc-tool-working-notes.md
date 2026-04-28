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

> _What problem does this tool solve? Write 2–3 sentences describing the real-world utility of the tool you are building._

> Requirement is to build my version of the `wc` tool which is found in Unix and Linux. It must be able to replicate the functionalities of the
> actual `wc` tool.

- **Inputs:** The contents of the file to be processed OR standard input
- **Outputs:** Based on the option provided, for the given file, the tool should return
  - Number of bytes
  - Number of characters
  - Number of words
  - Number of newlines
- **Constraints:**

---

## 3. Initial Thoughts

_Before writing any code — what is your gut instinct? This section is for thinking out loud._

- **First approach considered:**
  - For all steps from 1 to 6, standard approach would be to read the file into a very long string and then do the count checks as per provided options, but this runs the risk of Out-Of-Memory (OOM) if the file is too large (Not sure about the limit - need to test it)
  - Possible approach - read in streaming or chunks, and read in binary format (binary format is needed to count the number of bytes)
- **What's confusing or unclear:**
- **Wrong paths you anticipated or tried:**

---

## 4. Goals & Success Criteria

### Goals

- Understand the core mechanics behind `wc`
- Practice file parsing, standard input parsing and error handling
- Produce a working CLI tool that mirrors real-world behavior for the required functionalities

### Success Criteria

- [ ] All required steps from the challenge pass
- [ ] Output matches the reference tool on test inputs
- [ ] Edge cases are handled gracefully (empty files, bad flags, large inputs)
- [ ] Code is clean, readable, and reasonably documented

---

## 5. Scope

### In Scope

For every input file or standard input, count and return the following:

- Number of bytes
- Number of characters
- Number of words
- Number of newlines

### Out of Scope

- Performance optimization beyond functional correctness
- GUI or web interface
- The `max-line-length` functionality in the original `wc` tool

---

## 6. Functional Requirements

_List each step from the challenge as a requirement. Add sub-bullets for specific behaviors._

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

_Briefly describe how you plan to structure the solution._

```
main.py       — Entry point, argument parsing, File / stdin reading logic, Primary processing logic, Output formatting
```

### Key Data Structures

- e.g. `Stats { lines: u64, words: u64, bytes: u64 }`

### Algorithm / Logic Notes

- e.g. "Count bytes using raw byte length, not character count, to match `wc -c` behavior"

### Non-Functional Requirements

| Requirement        | Detail                                              |
| ------------------ | --------------------------------------------------- |
| **Dependencies**   | stdlib only                                         |
| **Platform**       | cross-platform                                      |
| **Performance**    | e.g. must handle files up to 1 GB without crashing  |
| **Error Handling** | Exit with non-zero code on failure; print to stderr |

---

## 8. Implementation

### v1 — Working Solution

_Describe your initial approach and paste or link your first working version._

- **Approach:**
- **Key decisions made:**

```
# v1 solution here
```

### Refactoring Notes

_What did you clean up after getting it working?_

- Renamed variables/functions:
- Broke into smaller units:
- Removed duplication:
- Simplified logic:

```
# refactored version here
```

---

## 9. Test Plan

| Test Case      | Input                    | Expected Output              | Status |
| -------------- | ------------------------ | ---------------------------- | ------ |
| Basic file     | `mytool test.txt`        | `7145 58164 342190 test.txt` | ⬜     |
| Stdin input    | `cat test.txt \| mytool` | Same counts, no filename     | ⬜     |
| Empty file     | `mytool empty.txt`       | `0 0 0 empty.txt`            | ⬜     |
| Missing file   | `mytool nofile.txt`      | Error message, exit 1        | ⬜     |
| Multiple files | `mytool a.txt b.txt`     | Per-file + total line        | ⬜     |

### Edge Cases

- [ ] Files with no newline at end of file
- [ ] Binary files / non-UTF-8 content
- [ ] Very large files (streaming vs. loading into memory)
- [ ] Flags passed in any order (e.g. `-wl` vs `-l -w`)
- [ ] No arguments provided — fallback to stdin

---

## 10. Performance & Complexity

### Time Complexity

- Best case:
- Worst case:

### Space Complexity

- Analysis:

### Scaling Thoughts

- What happens with very large inputs?
- Potential bottlenecks:
- Possible optimizations:

---

## 11. Real-World Considerations

_If this were production code, what would change?_

- **Error handling:**
- **Input validation:**
- **Logging / observability:**
- **Would this be part of a larger system?**

---

## 12. References & Resources

- **Challenge URL:** `https://codingchallenges.fyi/challenges/challenge-wc`
- **Reference Tool Man Page:**
  - `man wc`
  - https://realpython.com/read-write-files-python
  - https://realpython.com/working-with-files-in-python/
- **RFC / Spec (if applicable):**
- **Inspiration / Prior Art:** _Any repos, blog posts, or docs consulted_

---

## 13. Progress Log

| Date       | Time Spent | Notes                                                                                                                                       |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-27 | 1h 0m      | Started Step 0 — Basic setup, filled initial information in PRD                                                                             |
| 2026-04-28 | 1h 15m     | Completed Step 1 (Count number of bytes) and Step 2 (Count number of lines), along with `uv` based tool setup steps and initial README      |
| 2026-04-28 | 1h 0m      | Completed Step 3 (Count number of words) and Step 4 (Count number of characters), along with `uv` based tool setup steps and initial README |

**Total Time:** ~X hours

---

## 14. Retrospective

_Fill this in after completing the challenge._

## **What went well?**

## **What was harder than expected?**

## **What did I learn?**

## **What would I do differently next time?**
