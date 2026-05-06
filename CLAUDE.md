# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands

- Setup: `poetry install`
- Run all tests: `poetry run pytest`
- Run single test: `poetry run pytest tests/test_file.py::test_function`
- Coverage: `poetry run coverage run -m pytest && poetry run coverage report`
- Lint: `poetry run pylint src/`
- Format: `poetry run black src/ tests/`

## Architecture

The package exposes two symbols from `src/api_to_dataframe/__init__.py`:
- `ClientBuilder` — the main entry point
- `RetryStrategies` — enum alias for `models.retainer.Strategies`

**Request flow:**
1. `ClientBuilder.__init__` validates all parameters and stores config.
2. `ClientBuilder.get_api_data()` calls `GetData.get_response()` (a plain `requests.get` with `raise_for_status()`), then returns `.json()`.
3. `ClientBuilder.api_to_dataframe(response)` calls `GetData.to_dataframe()`, which wraps `pd.DataFrame(response)` and raises `ValueError` if the result is empty.

**Retry decorator (`models/retainer.py`):**
`@retry_strategies` is a function decorator applied to `get_api_data`. It reads `self.retry_strategy`, `self.retries`, and `self.delay` from the instance. Hard cap on retries is `Constants.MAX_OF_RETRIES = 5` (defined in `utils/__init__.py`). Available strategies: `NO_RETRY_STRATEGY` (raises immediately), `LINEAR_RETRY_STRATEGY` (`time.sleep(delay)`), `EXPONENTIAL_RETRY_STRATEGY` (`time.sleep(delay * retry_number)`).

**`to_dataframe` input shape:** `pd.DataFrame` is called directly on the response dict/list. For rows to be created correctly, the API must return a list of dicts. A plain `{}` response produces an empty DataFrame and raises `ValueError`.

## Testing

Tests use the `responses` library to mock HTTP calls. All test files live in `tests/`. `conftest.py` inserts `src/` into `sys.path` so the in-development package is imported instead of any installed version.

## Code Style

- Python 3.10+ (minimum; EOL versions are dropped promptly)
- Type hints required on all function signatures
- black formatting, max line length 88
- snake_case for variables/functions, PascalCase for classes

## Versioning & Release

- Version is set manually in `pyproject.toml` (`version = "X.Y.Z"`).
- The CD workflow (`publish` job) triggers on every push to `main`, extracts the version with `poetry version -s`, creates a GitHub release, and publishes to PyPI. **The version must be bumped before merging or the CD action will not publish a new release.**
- `auto_version_bump.sh` exists but is commented out in `.pre-commit-config.yaml`; do not rely on it.
