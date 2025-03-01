# ADR 0003: JWT for Authentication

## Status
Accepted

## Context
We need a stateless, scalable authentication mechanism for our API that can handle both customer and admin authentication needs.

## Decision
We will implement JWT (JSON Web Tokens) for API authentication.

## Consequences
### Positive
- Stateless authentication reduces database load
- Easy to scale across multiple servers
- Built-in expiration mechanism
- Good support in Django REST Framework
- Suitable for mobile and web clients

### Negative
- Cannot invalidate individual tokens without additional complexity
- Token size larger than session IDs
- Need to handle token refresh mechanism