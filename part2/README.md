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

# HBnB - Simple Web Client (Part 4)

## Overview

This project is the front-end implementation of the HBnB application.
It focuses on building an interactive web client using HTML5, CSS3, and JavaScript (ES6).

The client communicates with a back-end API to provide features such as authentication, browsing places, viewing details, and adding reviews.

---

## Objectives

* Build a user-friendly interface
* Connect the front-end with back-end APIs
* Handle authentication using JWT
* Implement dynamic content using JavaScript
* Improve user experience without page reloads

---

## Learning Outcomes

* Use semantic HTML5 structure
* Apply modern CSS styling
* Work with Fetch API (AJAX)
* Handle cookies and sessions
* Manipulate the DOM dynamically
* Implement client-side filtering

---

## Project Structure

```
part4/
│
├── index.html
├── login.html
├── place.html
├── add_review.html
│
├── styles.css
├── scripts.js
│
└── images/
```

---

## Features

### Authentication

* User login using email and password
* JWT token stored in cookies
* Redirect after successful login
* Error handling for invalid credentials

---

### List of Places (index.html)

* Fetch places from API
* Display places as cards
* Show:

  * Name
  * Price per night
  * View details button
* Filter places by price (10, 50, 100, All)
* Hide login button if the user is authenticated

---

### Place Details (place.html)

* Display:

  * Name
  * Description
  * Price
  * Amenities
  * Reviews
* Fetch data using place ID from URL
* Show "Add Review" only for authenticated users

---

### Add Review (add_review.html)

* Submit review via API
* Accessible only for authenticated users
* Redirect unauthenticated users
* Display success or error messages

---

## Technologies Used

* HTML5
* CSS3
* JavaScript (ES6)
* Fetch API
* Cookies (JWT authentication)

---

## API Integration

Example request:

```javascript
fetch('https://your-api-url/places', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
```

---

## Cookie Handling

Store token:

```javascript
document.cookie = `token=${data.access_token}; path=/`;
```

Retrieve token:

```javascript
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) return value;
    }
    return null;
}
```

---

## CORS Configuration

If you encounter a CORS error, enable it in your Flask API:

```python
from flask_cors import CORS
CORS(app)
```

---

## Testing

* Test login with valid and invalid credentials
* Verify token storage in cookies
* Ensure correct redirection
* Validate filtering functionality
* Verify authentication restrictions

---

## Design Requirements

* Margin: 20px
* Padding: 10px
* Border: 1px solid #ddd
* Border radius: 10px

Classes used:

* place-card
* review-card
* details-button
* login-button
* place-details
* place-info

---

## Pages

| Page            | Description         |
| --------------- | ------------------- |
| login.html      | User authentication |
| index.html      | List of places      |
| place.html      | Place details       |
| add_review.html | Submit review       |

---

## Notes

* All pages are validated using W3C Validator
* UI updates dynamically without page reload
* Authentication controls access to features

---

## Author

Developed as part of the HBnB Project - Part 4
Holberton School

---

## Status

Completed
Ready for QA Review
