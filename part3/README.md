# HBnB - Part 2

This directory contains the implementation of the HBnB application (Part 2).

It follows a modular layered architecture:

- **Presentation Layer**: `hbnb/app/api/` (Flask-RESTx endpoints, versioned under `v1/`)
- **Business Logic Layer**: `hbnb/app/models/` (domain models with validation and relationships)
- **Service Layer (Facade)**: `hbnb/app/services/` (Facade pattern to connect layers)
- **Persistence Layer**: `hbnb/app/persistence/` (in-memory repository for Part 2; SQLAlchemy in Part 3)

---

## Installation

From inside the `part2` directory:

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

From inside the `part2` directory:

```bash
python run.py
```

The server will start at:

```
http://127.0.0.1:5000
```

Swagger API documentation is available at:

```
http://127.0.0.1:5000/api/v1/
```

---

## Run Tests

Make sure you are inside the `part2` directory.

Set PYTHONPATH (Windows PowerShell):

```bash
$env:PYTHONPATH="."
```

Then run:

```bash
pytest -q
```

---

## Implemented Features

- CRUD endpoints for Users
- CRUD endpoints for Amenities
- CRUD endpoints for Places
- CRUD endpoints for Reviews (DELETE supported for Review only)
- Model-level validation
- Relationship handling between User, Place, Review, and Amenity
- In-memory repository (Part 2 persistence)