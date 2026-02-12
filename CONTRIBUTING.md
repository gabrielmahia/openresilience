# Contributing to OpenResilience

Thank you for your interest in contributing to OpenResilience.

## How to Contribute

1. **Open an Issue first.** All non-trivial changes must begin with a GitHub Issue describing the problem or proposal. Do not submit a Pull Request without a linked Issue.

2. **Fork and branch.** Create a feature branch from `main`. Use a descriptive branch name (e.g., `fix/scoring-threshold`, `feat/chirps-adapter`).

3. **Keep changes small and focused.** One concern per Pull Request. Large refactors require prior discussion and maintainer approval.

4. **Follow existing code style.** Run `ruff check .` before submitting. All CI checks must pass.

5. **Add tests for new logic.** Any new pure-logic function must include at least one test. UI-only changes do not require tests but must not break existing ones.

6. **Sign off your commits.** By submitting a PR you agree that your contribution is provided under the project's Apache-2.0 License.

## What We Accept

- Bug fixes with reproduction steps
- New data adapters (NASA, CHIRPS, etc.) following the adapter pattern in `worker/adapters/`
- Documentation improvements
- Test coverage improvements
- Accessibility and localization enhancements

## What Requires Discussion First

- Architectural changes
- New dependencies
- UI redesigns
- Changes to scoring algorithms or severity thresholds
- Anything that affects data interpretation by end users

## Code of Conduct

Respectful, constructive collaboration is required. See `CODE_OF_CONDUCT.md`.

## Questions?

Use the GitHub Issues tab.
