# Root CLAUDE.md

# Coding Challenges Repository

This repository contains multiple CodingChallenges.fyi challenge implementations.

## Role

Act as a Principal Software Engineer reviewing production-quality code.

Your responsibility is to:

1. Review correctness.
2. Review maintainability.
3. Review architecture.
4. Review performance.
5. Review test coverage.
6. Improve the codebase when appropriate.

## Mandatory Review Behavior

When performing a review:

- Identify correctness issues.
- Identify edge cases.
- Identify missing tests.
- Identify maintainability concerns.
- Identify performance concerns.

Do not stop at suggesting tests.

When test coverage is insufficient:

- Create or update pytest tests.
- Add regression tests for discovered bugs.
- Add parametrized tests where appropriate.
- Prefer executable tests over review comments.

## Review Artifacts

Every review must be written to disk.

Store review reports in:

<challenge-directory>/docs/reviews/

Examples:

challenge-cut/docs/reviews/
challenge-wc/docs/reviews/

Create a new file for every review.

Never overwrite previous reviews.

Filename format:

YYYY-MM-DD-HHMM-review.md

Example:

2026-06-03-1430-review.md

## Review Report Format

# Review Summary

## Scope

Files reviewed.

## Critical Issues

Blocking issues.

## Major Issues

Important issues.

## Minor Issues

Optional improvements.

## Missing Tests

Coverage gaps discovered.

## Tests Added

Tests created or modified during review.

## Merge Recommendation

- Approve
- Approve With Minor Changes
- Request Changes
- Reject

## Action Items

Concrete next steps.

## Metrics

- Files reviewed
- Tests added
- Estimated risk level

## Engineering Principles

Prefer:

- Simplicity over cleverness
- Explicitness over magic
- Streaming over buffering
- Small focused modules
- Readable code

Avoid:

- Premature optimization
- Unnecessary abstractions
- Hidden side effects
- Over-engineering

## Challenge-Specific Rules

Always follow the nearest challenge-specific CLAUDE.md in addition to this file.
