# Categories API

## Endpoints

### List Categories
GET `/api/v1/categories/`

Returns a list of all root categories (categories with no parent).

**Response Example:**
```json
[
    {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics",
        "description": "Electronic devices and accessories",
        "is_active": true,
        "children": [
            {
                "id": 2,
                "name": "Smartphones",
                "slug": "smartphones",
                "description": "Mobile phones and accessories",
                "is_active": true,
                "children": []
            }
        ]
    }
]
```

### Get Single Category
GET `/api/v1/categories/{slug}/`

Retrieves a specific category by its slug.

### Create Category
POST `/api/v1/categories/`

Creates a new category.

**Request Body:**
```json
{
    "name": "Electronics",
    "description": "Electronic devices and accessories",
    "parent": null,
    "is_active": true
}
```