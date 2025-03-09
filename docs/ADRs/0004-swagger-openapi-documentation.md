# ADR 0004: Swagger/OpenAPI for API Documentation

## Status
Accepted

## Context
We need comprehensive, interactive API documentation that is always in sync with the codebase.

## Decision
We will use Swagger/OpenAPI (via drf-yasg) for API documentation.

## Consequences
### Positive
- Auto-generated documentation from code
- Interactive API testing interface
- Industry-standard format
- Easy export to other formats
- Supports multiple UI options (Swagger UI, ReDoc)

### Negative
- Additional decorators needed for complete documentation
- Some manual maintenance required for complex endpoints
- Slight performance overhead in development