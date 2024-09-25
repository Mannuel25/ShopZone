# 🛒 ShopZone API

## Overview 📋

ShopZone is a API for an e-commerce platform designed to provide users with the ability to manage products, create accounts, and perform authenticated operations. This API supports product CRUD operations, role-based access control (RBAC), JWT-based authentication, and caching for performance optimization. 

With ShopZone, users can:
- Register, log in, and manage their own product listings.
- Filter products and securely interact with store data.
- Benefit from the integration of third-party services such as currency conversion.

Built with **Django**, **Django REST Framework**, and **PostgreSQL**, the platform leverages **Redis** for caching and supports **JWT** for secure access. It is designed with performance optimization in mind, ensuring fast and efficient interactions.

---

## Key Features ⭐

- **User Registration & Authentication**: 
  - Users can sign up using email, username, and password.
  - Secure authentication using JWT with login and logout functionality.

- **Product Management**:
  - Full support for **CRUD** (Create, Read, Update, Delete) operations on products.
  - Each product includes attributes such as name, description, price, quantity, category, and store ID.
  - Only authenticated users can create, update, and delete products.

- **Role-Based Access Control (RBAC)**:
  - Two user roles: **Admin** and **User**.
  - Admins can manage all products and users, while regular users can only manage their own products.
  
- **Database Management**:
  - Uses **PostgreSQL** for storing user and product data.
  - Includes database migrations to set up and modify schemas as needed.
  
- **Performance Optimization**:
  - **Caching** is implemented for frequently accessed product data using **Redis** to ensure high-performance API responses.
  
- **Third-Party Integration**:
  - Integration with a currency conversion API to convert product prices to different currencies, offering flexibility to users globally.

- **Testing**:
  - Includes unit and integration tests for user registration, authentication, and product management using **PyTest** to ensure code reliability and maintainability.

---

## Technologies Used 🛠️

- **Django**: Backend web framework to power the API.
- **Django REST Framework**: Provides tools to build a RESTful API with authentication and authorization features.
- **PostgreSQL**: A relational database system for managing and storing data.
- **Redis**: An in-memory data structure store, used here for caching frequently accessed product data.
- **JWT**: JSON Web Tokens for secure, stateless user authentication.

---

## Project Setup 🏗️

### Prerequisites

- **Python 3.6+**
- **PostgreSQL**
- **Redis**
- **pip** (Python package installer)

### Installation

### Option 1: Manual Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mannuel25/shopzone.git
   cd shopzone
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the Database**:
   Update the `DATABASES` settings in `shopzone/settings.py` to match your PostgreSQL configuration.

6. **Make Migrations**

   ```bash
   python manage.py makemigrations
   ```

7. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

8. **Create a Superuser (Optional)**

   ```bash
   python manage.py createsuperuser
   ```

9. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```


---

### Option 2: Docker Setup 🐳

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mannuel25/ShopZone.git
   cd ShopZone
   ```

2. **Ensure Docker is installed**

   Ensure Docker and Docker Compose are installed and running on your machine. You can check this with the following commands:

   ```bash
   docker --version
   docker-compose --version
   ```

3. **Build and Start the Docker Containers**

   Use Docker Compose to build the containers and start the services:

   ```bash
   docker-compose up --build
   ```

4. **Make Migrations**

   Once the containers are up, make the migrations to set up the database schema:

   ```bash
   docker-compose exec web python manage.py makemigrations
   ```

5. **Run Migrations**

   Once the containers are up, apply the migrations to set up the database schema:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create a Superuser (Optional)**

   If you want to create a superuser, run:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Access the Application**

   After successfully running the Docker containers, the application will be available at:

   ```bash
   http://localhost:8000
   ```

8. **Stop the Docker Containers**

   When you're done, stop the containers using:

   ```bash
   docker-compose down
   ```


---

## API Documentation 📖

Explore the API using the Postman collection [here](https://www.postman.com/lunar-rocket-946206/workspace/shopzone/collection/20593383-4e119c8d-ade5-4eeb-881c-0de7231f9da5?action=share&creator=20593383) for testing and interacting with the API endpoints.
Alternatively, you can interact with the documentation available at `/swagger/` or `/redoc/` endpoints when running the server.


---

## Integration with a Third-Party API 🌍

- **Currency Conversion**: Products can be priced in different currencies by integrating with the [ExchangeRate API](https://www.exchangerate-api.com/docs/overview). This allows customers to view product prices in their preferred currency, providing flexibility for global transactions. You can refer to the [supported currencies list](https://www.exchangerate-api.com/docs/supported-currencies) to see the available currencies for filtering.
---

## Testing 🧪

Run the tests to ensure the system is functioning as expected:

  ```bash
  pytest
  ```

---

## Error Handling 🚨

Errors are returned in the following format:

```json
{
    "message": "Error message",
    "status_code": 400
}
```

---


## License 📜

This project is licensed under an  [MIT LICENSE](LICENSE).

