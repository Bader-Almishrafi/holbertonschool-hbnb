# HBnB Part 2 - Testing & Validation Report (Task 6)

## Environment
- OS: Windows
- Shell: Git Bash / PowerShell
- Python: 3.x
- Framework: Flask + Flask-RESTx
- Storage: InMemoryRepository (data resets on server restart)

## Swagger Documentation
- URL: http://127.0.0.1:5000/api/v1/
- Namespaces: users, amenities, places, reviews

## Validation Implemented (Model Level)
### User
- first_name required, max 50
- last_name required, max 50
- email required, valid format
- email uniqueness (in-memory)
- is_admin boolean

### Amenity
- name required, max 50

### Place
- title required, max 100
- price non-negative number
- latitude in [-90, 90]
- longitude in [-180, 180]
- owner must be a valid User instance

### Review
- text required
- rating integer (accepts 5 or 5.0), range [1..5]
- place must be valid Place instance
- user must be valid User instance

## Manual Black-Box Tests (cURL)
> Note: Manual tests were executed in sequence (User -> Amenity -> Place -> Review) due to entity relationships.

### Users
- POST /api/v1/users/ (valid) -> 201
- POST /api/v1/users/ (invalid email) -> 400
- GET /api/v1/users/<fake> -> 404
- PUT /api/v1/users/<id> (valid) -> 200

### Amenities
- POST /api/v1/amenities/ (valid) -> 201
- POST /api/v1/amenities/ (empty name) -> 400
- GET /api/v1/amenities/<fake> -> 404

### Places
- POST /api/v1/places/ (valid with owner_id + amenities) -> 201
- POST /api/v1/places/ (invalid latitude) -> 400
- GET /api/v1/places/<fake> -> 404
- GET /api/v1/places/<id> includes owner, amenities, reviews -> 200

### Reviews
- POST /api/v1/reviews/ (valid) -> 201
- POST /api/v1/reviews/ (invalid rating=6) -> 400
- GET /api/v1/places/<place_id>/reviews -> 200
- DELETE /api/v1/reviews/<id> -> 200
- GET /api/v1/reviews/<id> after delete -> 404

## Automated Tests (pytest)
- Command: `pytest -q`
- Coverage:
  - user creation valid/invalid, not found
  - amenity valid/invalid
  - place invalid latitude
  - review create/list/update/delete flow
- Result:
  - (paste your pytest output here)