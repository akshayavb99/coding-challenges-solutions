# .claude/skills/code-reviewer/SKILL.md

# Coding Challenge Reviewer

Use this skill whenever reviewing a CodingChallenges.fyi implementation.

## Review Priorities

1. Correctness
2. Behavior parity with reference utility
3. Edge cases
4. Test coverage
5. Maintainability
6. Performance

## Mandatory Actions

If missing tests are discovered:

- Create pytest tests.
- Prefer parametrized tests.
- Add regression tests for bugs.
- Add integration tests when behavior spans modules.

## Test Categories

Review coverage for:

- Happy paths
- Invalid input
- Boundary conditions
- Empty input
- Large input
- File input
- stdin input
- CLI argument parsing
- Error handling

## Performance Review

Assess:

- Time complexity
- Memory usage
- Streaming behavior
- Large file handling

## Output Expectations

Every review should:

- Produce a review report.
- Update tests when needed.
- Explain risk level.
- Provide merge recommendation.

Default recommendation:

Request Changes

until confidence is high.
