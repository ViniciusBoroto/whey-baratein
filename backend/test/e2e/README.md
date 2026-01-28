# E2E Testing Guide

## What are E2E Tests?

**End-to-End (E2E) tests** verify the complete application flow from HTTP request to database and back. They test the entire stack working together, ensuring all components integrate correctly.

## Key Principles

### 1. **Real HTTP Requests**
- Use `TestClient` from FastAPI to make actual HTTP calls
- Test the full request/response cycle including middleware, routing, and serialization

### 2. **Real Database**
- Use **testcontainers** to spin up isolated PostgreSQL instances
- Each test gets a fresh database (function scope)
- No mocking of database layer - test actual SQL queries

### 3. **Test Isolation**
- Each test is independent
- Fresh database per test prevents data pollution
- Tests can run in any order

### 4. **Minimal Mocking**
- Only mock external services (payment gateways, email, etc.)
- Don't mock your own code - test the real implementation

### 5. **Test Authentication & Authorization**
- Create JWT tokens for different user roles
- Test protected endpoints with proper credentials
- Verify authorization rules (admin vs user permissions)

## Project Structure

```
test/
├── e2e/
│   ├── conftest.py              # Shared fixtures
│   ├── test_auth_routes.py      # Login tests
│   ├── test_user_routes.py      # User CRUD tests
│   ├── test_brand_routes.py     # Brand CRUD + auth tests
│   └── test_whey_routes.py      # Whey CRUD + complex auth tests
```

## How It Works

### conftest.py Setup

1. **PostgreSQL Container**: Spins up isolated database
2. **Engine & Session Factory**: Creates SQLAlchemy connections
3. **TestClient**: FastAPI test client with dependency overrides
4. **Token Fixtures**: Pre-generated JWT tokens for admin/user roles

### Dependency Override Pattern

```python
app.dependency_overrides[get_user_usecases] = override_user_usecases
```

This ensures tests use the test database instead of production database.

## Test Categories

### 1. **Happy Path Tests**
- Valid requests with correct data
- Successful CRUD operations
- Proper authentication

### 2. **Error Cases**
- Invalid credentials (401)
- Unauthorized access (403)
- Not found errors (404)
- Duplicate data conflicts

### 3. **Authorization Tests**
- Admin-only endpoints
- User ownership validation
- Cross-user access prevention

## Running Tests

```bash
# Run all e2e tests
pytest test/e2e/

# Run specific test file
pytest test/e2e/test_user_routes.py

# Run with verbose output
pytest test/e2e/ -v

# Run specific test
pytest test/e2e/test_auth_routes.py::test_login_success
```

## Best Practices

### ✅ DO:
- Test complete user flows (create user → login → create resource)
- Verify response status codes AND response bodies
- Test both success and failure scenarios
- Use descriptive test names
- Keep tests independent

### ❌ DON'T:
- Share state between tests
- Mock your own repositories/services
- Skip error case testing
- Hardcode IDs (use created resources)
- Test implementation details

## Example Test Pattern

```python
def test_create_and_retrieve_resource(client, admin_token):
    # 1. Setup: Create dependencies
    brand = client.post("/api/v1/brands", 
        json={"name": "Test Brand", ...},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    brand_id = brand.json()["id"]
    
    # 2. Action: Create main resource
    response = client.post("/api/v1/whey",
        json={"name": "Test Whey", "brand_id": brand_id, ...},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # 3. Assert: Verify creation
    assert response.status_code == 201
    whey_id = response.json()["id"]
    
    # 4. Verify: Retrieve and check persistence
    get_response = client.get(f"/api/v1/whey/{whey_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Whey"
```

## Coverage

The e2e tests cover:

- ✅ **Auth Routes**: Login with valid/invalid credentials
- ✅ **User Routes**: Create, read, delete users
- ✅ **Brand Routes**: Full CRUD with admin authorization
- ✅ **Whey Routes**: Complex authorization (admin vs owner vs other users)

## Why Testcontainers?

- **Isolation**: Each test gets fresh database
- **Reproducibility**: Same environment every time
- **CI/CD Ready**: Works in Docker environments
- **No cleanup needed**: Container destroyed after test
- **Real database**: Tests actual PostgreSQL behavior

## Performance Tips

- Use `scope="function"` for isolation (current setup)
- Consider `scope="module"` for faster tests (shared DB per file)
- Run tests in parallel: `pytest -n auto` (requires pytest-xdist)
