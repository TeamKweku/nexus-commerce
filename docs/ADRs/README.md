# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for the E-Commerce Platform Backend project.

## What is an ADR?
An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

## ADR Index

1. [Use Django REST Framework](0001-use-django-rest-framework.md)
2. [PostgreSQL as Primary Database](0002-postgresql-database.md)
3. [JWT for Authentication](0003-jwt-authentication.md)
4. [Swagger/OpenAPI for API Documentation](0004-swagger-openapi-documentation.md)
5. [Role-Based Access Control](0005-role-based-access-control.md)

## Template
When creating a new ADR, use the following template:

```markdown
# ADR {NUMBER}: {TITLE}

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[Description of the context and problem statement]

## Decision
[Description of the decision made]

## Consequences
### Positive
- [Positive consequence 1]
- [Positive consequence 2]

### Negative
- [Negative consequence 1]
- [Negative consequence 2]
```