# HBnB - Part 2 (Project Setup)

This directory contains the initial project setup for the HBnB application (Part 2).
It follows a modular layered architecture:

- **Presentation Layer**: `hbnb/app/api/` (Flask-RESTx endpoints, versioned under `v1/`)
- **Business Logic Layer**: `hbnb/app/models/` (domain models - placeholders for now)
- **Service Layer (Facade)**: `hbnb/app/services/` (Facade pattern to connect layers)
- **Persistence Layer**: `hbnb/app/persistence/` (in-memory repository for Part 2; SQLAlchemy in Part 3)

## Install
```bash
pip install -r requirements.txt
