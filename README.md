# Django E-Commerce Platform Backend

A scalable Django e-commerce backend with REST APIs, JWT auth, and advanced product discovery features.

## 🌟 Features

- **RESTful APIs**: Complete CRUD operations for products, categories, and user accounts
- **Advanced Product Discovery**: Filtering, sorting, and pagination capabilities
- **Secure Authentication**: JWT implementation with role-based access control
- **Database Optimization**: Efficient PostgreSQL schema with proper indexing
- **API Documentation**: Interactive Swagger/OpenAPI integration

## 🛠️ Tech Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Swagger/OpenAPI

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Git

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/django-ecommerce-backend.git
   cd django-ecommerce-backend
   ```

2. Set up a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   ```bash
   cp .envs/.env.example .env
   # Edit .env with your database credentials and other settings
   ```

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/

## 🧪 Running Tests

```bash
python manage.py test
```

## 📋 Project Structure

The project structure will be updated as the codebase develops.

## 🔒 Security Notes

- The default Django secret key should be changed in production
- Debug mode should be disabled in production
- JWT tokens should have appropriate expiration times

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
