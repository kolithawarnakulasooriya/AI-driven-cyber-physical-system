# Code Style Rules

- Follow PEP 8 for Python code.
- Use explicit type hints for function arguments and return values.
- Keep line length <= 100 characters; wrap lines using black.
- Prefer f-strings over `.format()` or `%` formatting.
- Use single spaces around operators and after commas.
- Import statements must be ordered: standard library, third-party, local modules; each group separated by a blank line.
- All modules must include a docstring that describes purpose and public API.
- Use descriptive, lowercase-with-underscores names for variables and functions.
- Do not use wildcard imports (`from module import *`).
- Add `# noqa` only as a last resort; address the underlying issue instead.
- Write unit tests for all new public functions and classes.
- Run the linter (`flake8`) and formatter (`black`) before committing.