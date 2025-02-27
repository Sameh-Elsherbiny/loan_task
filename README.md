# Loan Management System

This is a Django-based Loan Management System that allows users to manage loans, loan plans, and repayments. The project includes models for `LoanPlan`, `Loan`, `LoanCustomer`, `LoanProvider`, `Bank`, and `MonthlyRepayment`. It also includes serializers and unit tests for these models.

## Features

- User management with custom user types (`LoanCustomer`, `LoanProvider`, `Bank`)
- Loan management with validation and constraints
- Monthly repayment tracking with penalty checks
- REST API for managing loans and users
- Unit tests for models and serializers

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```sh
git clone https://github.com/yourusername/loan-management-system.git
cd loan-management-system

Build and Run the Project
Use Docker Compose to build and run the project:
```sh
docker-compose up --build
```

This command will build the Docker images and start the containers for the Django application, MySQL database, and Redis.

Apply Migrations
After the containers are up and running, apply the database migrations:

```sh
docker-compose exec web python manage.py migrate
```

Create a Superuser
Create a superuser to access the Django admin interface:
```sh
docker-compose exec web python manage.py createsuperuser
```

Access the Application
The Django application will be available at http://localhost:8000.
The Django admin interface will be available at http://localhost:8000/admin.
Running Tests
To run the unit tests, use the following command:
```sh
docker-compose exec web python manage.py test
```

Project Structure
loan: Contains the loan management app with models, serializers, views, and tasks.
users: Contains the user management app with custom user models and serializers.
tests/: Contains unit tests for the project.
Dockerfile: Dockerfile for building the Django application image.
docker-compose.yml: Docker Compose file for setting up the development environment.
