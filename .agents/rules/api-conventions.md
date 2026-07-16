# API Conventions

## General Principles
- All public APIs must be versioned under `/v1/` in the request path.
- Use plural nouns for resource collections (e.g., `/v1/sensors`).
- Singular nouns represent individual resources (e.g., `/v1/sensor/{id}`).

## Request Format
- HTTP methods map to CRUD semantics: `GET` for retrieval, `POST` for creation, `PUT` for replacement, `PATCH` for partial updates, `DELETE` for removal.
- Input data must be JSON; accept only `application/json` content type.
- Query parameters are used for filtering, pagination, and optional fields; they must be documented in the API spec.
- Error payloads must follow the structure:
  ```json
  {
    "error": "string",
    "code": "string",
    "details": {}
  }
  ```

## Response Format
- Successful responses use appropriate HTTP status codes (200, 201, 204).
- Resource representations must include a self-link (`"self": "/v1/sensor/123"`), a `"type"` identifier, and a `"attributes"` object.
- Lists include a `"meta"` field with pagination info (`total`, `limit`, `offset`).

## Error Handling
- Raise validation errors with HTTP 400 and include a list of field‑specific messages.
- Unauthenticated access returns 401 with `"code": "UNAUTHORIZED"`.
- Missing permissions return 403 with `"code": "FORBIDDEN"`.
- Unexpected server errors return 500 with a generic `"code": "INTERNAL_ERROR"`; internal details are omitted from the response body.

## Versioning & Deprecation
- New major versions are released under a new major semver (`vX.Y.Z → vX+1.Y.Z`).
- Deprecation notices are added to the API documentation and header `Deprecation: true` for at least 90 days before removal.
- Backward‑compatible changes are introduced as minor versions (`v1.0 → v1.1`).

## Naming Conventions
- Functions exposed via the API must use lower‑case snake_case in the URL path.
- Query parameter names must be lowercase and singular when representing a single identifier (e.g., `id`, `sensor_id`).
- Field names in JSON responses are snake_case, matching the underlying data model.

## Authentication
- Use API keys passed in the `Authorization: Bearer <token>` header.
- Tokens must be JWTs signed with HS256; include `exp`, `iat`, and `scope` claims.
- Tokens are issued via `/v1/auth/token` with a valid client credential payload.

## Testing Conventions
- All API endpoints must have associated unit tests covering success and error paths.
- Integration tests should mock external dependencies and run against a disposable test database.
- Test names must follow the pattern `test_<endpoint>_<scenario>_<expected_result>`.