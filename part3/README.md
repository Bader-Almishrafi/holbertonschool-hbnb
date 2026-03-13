# HBnB - Part 3

This part of the HBnB project focuses on improving the backend by adding authentication, role-based access control, database persistence using SQLAlchemy, and defining relationships between entities.

The goal of this part is to move from an in-memory storage system to a real database while maintaining a clean architecture using the repository and service patterns.

---

# Features Implemented

### Authentication with JWT

JWT authentication was implemented to secure endpoints.  
Only authenticated users can create and modify resources.

Protected endpoints include:

- Creating places
- Updating places
- Creating reviews
- Updating reviews
- Deleting reviews
- Updating user information

Public endpoints remain accessible without authentication.

---

### Administrator Access Control

Role-based access control (RBAC) was added to allow administrators to perform privileged actions.

Administrators can:

- Create new users
- Modify any user information
- Add new amenities
- Modify amenities
- Bypass ownership restrictions for places and reviews

Admin privileges are checked using JWT claims.

---

### SQLAlchemy Persistence Layer

The in-memory repository was replaced with a SQLAlchemy-based repository to persist data in a relational database.

Key components include:

- `SQLAlchemyRepository` for generic CRUD operations
- `UserRepository` for user-specific queries
- Integration with the application facade

SQLite is used as the development database.

---

### Database Models

The following entities were mapped using SQLAlchemy:

- **User**
- **Place**
- **Review**
- **Amenity**

Each model includes validation logic and integrates with the BaseModel class that provides:

- UUID identifiers
- created_at timestamp
- updated_at timestamp

---

### Relationships Between Entities

The following relationships were implemented:

**User → Place (One-to-Many)**  
A user can own multiple places.

**User → Review (One-to-Many)**  
A user can write multiple reviews.

**Place → Review (One-to-Many)**  
A place can have multiple reviews.

**Place ↔ Amenity (Many-to-Many)**  
A place can have multiple amenities and an amenity can belong to multiple places.

This relationship is implemented using the `place_amenity` association table.

---

### SQL Database Schema

Raw SQL scripts were created to generate the database schema without using the ORM.

Tables included:

- users
- places
- reviews
- amenities
- place_amenity

Constraints include:

- Foreign keys
- Unique constraints
- Composite primary keys
- Rating validation (1–5)

Initial data includes:

- Administrator user
- Default amenities

---

### ER Diagram

An Entity-Relationship diagram was generated using Mermaid.js to visualize the database structure.

Entities represented:

- USERS
- PLACES
- REVIEWS
- AMENITIES
- PLACE_AMENITY

The diagram reflects the relationships implemented in the SQLAlchemy models.

---

# Technologies Used

- Python
- Flask
- Flask-RESTx
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLAlchemy
- SQLite
- Mermaid.js

---

# Authors

HBnB Project - Holberton School