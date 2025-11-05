# Unipile API Client To-Do List

## Phase 1: Core Refactoring and Cleanup

### 1.1 Project Structure & Dependencies

- [x] Add `pyproject.toml` for packaging and dependency management (`uv`).
- [ ] Refactoring tools initialize (dev)
- [ ] Move project specific files into unipile_sdk
- [ ] Test quickstart
- [ ] Verify models files, remove `models_old.py`
- [ ] Add `__version__` to `__init__.py`.

### 1.2 Code Cleanup

- [ ] Remove unused imports and variables across the project.
- [ ] Configure tooling: ruff + mypy, basedpyright, vulture, pyupgrade, trailing-whitespace, end-of-file-fixer

### 1.3 Model Improvements

- [ ] Replace all `Any` type hints with specific types.
- [ ] Use Pydantic's `Field` for validation.
- [ ] Consolidate duplicated enums.
- [ ] Complete the `LinkedinSalesNavSearchPayload` model.

## Phase 2: API Client Implementation and Error Handling

### 2.1 Client Implementation

- [ ] Implement `_verify_connected_account` in `AsyncClient`.
- [ ] Remove the unused `auth` parameter from `AsyncClient.request`.
- [ ] Move query `None`-filtering to `BaseClient._build_request`.

### 2.2 API Endpoint Implementation

- [ ] Implement `before`/`after` support in `MessagesEndpoint.messages`.
- [ ] Implement `HostedEndpoint.retrieve`.
- [ ] Simplify and validate `limit` handling in `SearchEndpoint.search`.

### 2.3 Error Handling

- [ ] Add more specific exception types (e.g., `RateLimitError`).
- [ ] Include more context in error messages.

### 2.4 Configuration

- [ ] Use `pydantic-settings` for configuration and environment variables.
- [ ] Add validation for configuration options.

## Phase 3: Testing

### 3.1 Framework Setup

- [ ] Set up `pytest` and `pytest-recording` (for caching), maybe `pytest-asyncio`, `pytest-httpx`, and `pytest-cov`.
- [ ] Automatic tests on multiple python versions

### 3.2 Test Suites

- [ ] **Models (`tests/test_models.py`)**
    - [ ] Test model creation, serialization, and validation.
- [ ] **Client (`tests/test_client.py`)**
    - [ ] Test client instantiation, request building, response parsing, and error handling.
- [ ] **API Endpoints (`tests/test_endpoints.py`)**
    - [ ] Test each endpoint method for correct behavior and error handling.
- [ ] **Helpers (`tests/test_helpers.py`)**
    - [ ] Test all helper functions.

### 3.3 Integration tests

- [ ] Test async search with more than 50 requests for pagination and rate limiting.
- [ ] Verify full workflow: authentication, request sending, and response handling.
- [ ] Test error scenarios: invalid authentication, rate limits, and network failures.
- [ ] Record general and features related demo videos

## Phase 4: Documentation and Examples

### 4.1 Docstrings

- [ ] Fix/verify all links in docstrings.
- [ ] Ensure consistent docstring style.
- [ ] Add examples to docstrings.

### 4.2 API Documentation

- [ ] Examples directory
- [ ] Generate API documentation using `swagger`?.
