# signal-utils

Small MATLAB utilities for unit conversion and signal smoothing.

- `src/` — library functions
- `tests/` — unit tests (MATLAB unit testing framework)
- `buildfile.m` — build plan with `check` (code issues) and `test` tasks

Build and test locally from the repository root:

```matlab
buildtool check test
```

CI runs the build on GitHub Actions — see `.github/workflows/ci.yml`.
