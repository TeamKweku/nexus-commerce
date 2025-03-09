# NexusCommerce: Django E-Commerce Platform Backend

A scalable, feature-rich Django e-commerce backend with comprehensive REST APIs, JWT authentication, and advanced product discovery capabilities.

## 📚 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)

## 🌟 Features

### Core Functionality
- **RESTful APIs**: Complete CRUD operations for products, categories, and user accounts
- **Advanced Product Discovery**: 
  - Multi-criteria filtering
  - Dynamic sorting (price, popularity, relevance)
  - Efficient pagination for large catalogs
- **Secure Authentication**: 
  - JWT implementation
  - Role-based access control (RBAC)
  - Custom user roles and permissions

### Technical Features
- **Database Optimization**: 
  - Efficient PostgreSQL schema
  - Strategic indexing
  - Query optimization
- **API Documentation**: 
  - Interactive Swagger/OpenAPI interface
  - ReDoc alternative view
- **Security**: 
  - JWT token management
  - Role-based permissions
  - Secure password handling

## 🏗 Architecture

### Project Structure
```
nexuscommerce/
├── core_apps/           # Core application modules
│   ├── products/        # Product management
│   ├── categories/      # Category management
│   └── profiles/        # User profiles
├── config/              # Project configuration
├── docs/                # Documentation
│   ├── ADRs/           # Architecture Decision Records
│   └── ERDs/           # Database schemas
└── tests/               # Test suite
```

### Key Components
- **Product Management**: Handles product CRUD operations and discovery
- **Category System**: Manages hierarchical product categorization
- **User Management**: Handles authentication and authorization
- **API Layer**: RESTful interface using Django REST Framework

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Documentation**: Swagger/OpenAPI
- **Testing**: pytest
- **CI/CD**: GitHub Actions

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL
- Docker & Docker Compose (recommended)

### Installation

#### Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/nexuscommerce.git
cd nexuscommerce

# Copy environment variables
cp .envs/.env.example .env

# Build and start services
make build
make migrate
make superuser
```

#### Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/local.txt

# Configure environment
cp .envs/.env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Configuration
Key environment variables (in `.env`):
```
DJANGO_SECRET_KEY=your-secret-key
POSTGRES_DB=nexuscommerce
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
```

## 📖 API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

### Example API Endpoints
```bash
# Authentication
POST /api/auth/token/         # Obtain JWT token
POST /api/auth/token/refresh/ # Refresh JWT token

# Products
GET    /api/products/         # List products
POST   /api/products/         # Create product
GET    /api/products/{id}/    # Get product details
PUT    /api/products/{id}/    # Update product
DELETE /api/products/{id}/    # Delete product
```

## 💻 Development

### Code Style
- Black for formatting (max-line-length: 88)
- Flake8 for linting
- isort for import sorting

### Making Changes
1. Create a feature branch
2. Make your changes
3. Run tests: `pytest`
4. Submit a pull request

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core_apps

# Run specific test file
pytest tests/test_products.py
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick start:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## 🗺 Roadmap

### Current Sprint
- [ ] Fix phone number validation in profiles
- [ ] Improve Swagger documentation
- [ ] Add profile update audit logging

### Future Plans
- Shopping cart functionality
- Checkout process
- Order management
- Payment processing
- Email notifications
- Mobile app integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support, email teamkweku@outlook.com or open an issue.
