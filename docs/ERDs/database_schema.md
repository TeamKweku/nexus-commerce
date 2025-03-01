# E-Commerce Platform Database Schema

## 📊 Entity Relationship Diagram Documentation

### 🛍️ Product Management

#### Category
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `name` (varchar, required)
  - `slug` (varchar, unique, required)
  - `parent_id` (bigint, optional) → Self-reference to Category
  - `is_active` (boolean, default: true)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**: 
  - Unique: `slug`
  - Regular: `name`, `parent_id`, `is_active`, `(parent_id, is_active)`

#### Brand
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `name` (varchar, required)
  - `slug` (varchar, unique, required)
  - `logo` (varchar, optional)
  - `description` (text, optional)
  - `website` (varchar, optional)
  - `is_active` (boolean, default: true)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Unique: `slug`
  - Regular: `name`, `is_active`

#### Product
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `name` (varchar, required)
  - `slug` (varchar, unique, required)
  - `description` (text, required)
  - `short_description` (text, optional)
  - `brand_id` (bigint) → Brand
  - `product_type_id` (bigint) → ProductType
  - `is_digital` (boolean, default: false)
  - `is_active` (boolean, default: true)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Unique: `slug`
  - Regular: `name`, `brand_id`, `product_type_id`, `is_active`, `created_at`
  - Composite: `(is_active, product_type_id)`, `(is_active, brand_id)`, `(is_active, created_at)`

### 🏷️ Product Attributes

#### Attribute
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `name` (varchar, required)
  - `description` (text, optional)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Regular: `name`

#### AttributeValue
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `attribute_id` (bigint) → Attribute
  - `value` (varchar, required)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Unique: `(attribute_id, value)`
  - Regular: `attribute_id`

### 📦 Product Variants

#### ProductLine (Variant)
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `product_id` (bigint) → Product
  - `sku` (varchar, unique, required)
  - `price` (decimal, required)
  - `sale_price` (decimal, optional)
  - `stock_qty` (int, default: 0)
  - `weight` (decimal, optional)
  - `is_active` (boolean, default: true)
  - `order` (int, default: 1)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Unique: `sku`
  - Regular: `product_id`, `is_active`, `price`, `stock_qty`
  - Composite: `(product_id, is_active)`, `(is_active, stock_qty)`, `(product_id, order)`

### 👤 User Management

#### User
- **Primary Key**: `pkid` (bigint, auto-increment)
- **Fields**:
  - `id` (UUID, unique)
  - `first_name` (varchar(60), required)
  - `last_name` (varchar(60), required)
  - `email` (varchar, unique, required)
  - `username` (varchar(60), unique, required)
  - `password` (varchar, required)
  - `is_superuser`, `is_staff`, `is_active` (boolean)
  - `date_joined`, `last_login` (timestamp)
- **Indexes**:
  - Unique: `email`, `username`, `id`
  - Regular: `is_active`

#### Profile
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `user_id` (bigint) → User
  - `user_type` (varchar(20), default: "buyer")
  - `avatar` (varchar, optional)
  - `bio` (text, optional)
  - `phone_number` (varchar(30), optional)
  - `address` (varchar(255), optional)
  - `country` (varchar(2), default: "GH")
  - `city` (varchar(180), default: "Accra")
  - `slug` (varchar, unique)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Unique: `user_id`, `slug`
  - Regular: `user_type`, `country`, `city`
  - Composite: `(country, city)`

### 🔗 Junction Tables

#### ProductCategory
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `product_id` (bigint) → Product
  - `category_id` (bigint) → Category
- **Indexes**:
  - Unique: `(product_id, category_id)`
  - Regular: `product_id`, `category_id`

#### ProductLineAttributeValue
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `product_line_id` (bigint) → ProductLine
  - `attribute_value_id` (bigint) → AttributeValue
- **Indexes**:
  - Unique: `(product_line_id, attribute_value_id)`
  - Regular: `product_line_id`, `attribute_value_id`

### 🖼️ Media

#### ProductImage
- **Primary Key**: `id` (bigint, auto-increment)
- **Fields**:
  - `product_line_id` (bigint) → ProductLine
  - `name` (varchar, required)
  - `alternative_text` (varchar, optional)
  - `url` (varchar, required)
  - `is_feature` (boolean, default: false)
  - `created_at`, `updated_at` (timestamp)
- **Indexes**:
  - Regular: `product_line_id`
  - Composite: `(product_line_id, is_feature)`

## 📝 Notes

1. All timestamp fields (`created_at`, `updated_at`) are automatically managed
2. Soft deletion is not implemented - consider adding `deleted_at` fields if needed
3. UUID is used for public User identification while internal references use bigint
4. Proper indexing is in place for common query patterns
5. Foreign key constraints are enforced at the database level