# HBnB Plus

HBnB Plus is a polished Flask + Bootstrap project that upgrades the original Holberton part4 into an Airbnb-inspired booking platform.

## Highlights
- JWT authentication with register, login, and current-user endpoints
- Public place catalog with search by city, text, and max price
- Rich place details with reviews and guest capacity
- Booking system with check-in/check-out dates, guest count, total price, and overlap protection
- Admin dashboard with counts for users, places, reviews, bookings, and revenue
- Bootstrap frontend for home, login, register, place details, bookings, host view, and admin view
- SQLAlchemy persistence with demo seed data

## Demo credentials
- Admin: `admin@example.com` / `123456`
- Guest: `guest@example.com` / `123456`
- Host: `host@example.com` / `123456`

## Run
```bash
pip install -r requirements.txt
python run.py
```
Then open the static client files with a simple local server from the `client` folder, for example:
```bash
python -m http.server 8000
```
Open `http://127.0.0.1:8000/index.html`

## Main API routes
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET/POST /api/v1/places/`
- `GET/PUT/DELETE /api/v1/places/<id>`
- `GET /api/v1/places/<id>/reviews`
- `GET/POST /api/v1/reviews/`
- `GET/POST /api/v1/bookings/`
- `GET /api/v1/bookings/my-bookings`
- `GET /api/v1/admin/stats`

## Notes
- Existing `instance/development.db` may need to be deleted once if you are upgrading from the old schema so the new booking and place fields are created cleanly.
- Swagger docs are available at `http://127.0.0.1:5000/api/v1/`
