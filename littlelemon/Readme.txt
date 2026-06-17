## Little Lemon Restaurant – Back-End Capstone Project
=====================================================

### SETUP INSTRUCTIONS
------------------
1. Clone the repository:
   git clone <your-repo-url>
   cd littlelemon

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate           # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Create a MySQL database named "littlelemon":
   CREATE DATABASE littlelemon;

5. Update DATABASES credentials in littlelemon/settings.py if needed.

6. Run migrations:
   python manage.py migrate

7. Create a superuser:
   python manage.py createsuperuser

8. Start the development server:
   python manage.py runserver

NOTE: To run tests without MySQL, use SQLite:
   USE_SQLITE=1 python manage.py test restaurant


API PATHS TO TEST (with Insomnia or Postman)
--------------------------------------------

BASE URL: http://127.0.0.1:8000

── Static Page ──────────────────────────────
GET  /restaurant/                          → Home page (HTML)

── Authentication ───────────────────────────
POST /auth/users/                          → Register new user
     Body: { "username": "user1", "password": "Pass1234!" }

POST /auth/token/login/                    → Get auth token
     Body: { "username": "user1", "password": "Pass1234!" }
     Response: { "auth_token": "abc123..." }

POST /auth/token/logout/                   → Logout (invalidate token)
     Header: Authorization: Token <auth_token>

── Menu API (GET is public; write actions need token) ───
GET    /restaurant/menu/                   → List all menu items
POST   /restaurant/menu/                   → Create menu item (auth)
       Body: { "title": "Bruschetta", "price": "7.50", "inventory": 30 }

GET    /restaurant/menu/<id>/              → Retrieve single item
PUT    /restaurant/menu/<id>/              → Full update (auth)
PATCH  /restaurant/menu/<id>/              → Partial update (auth)
DELETE /restaurant/menu/<id>/              → Delete (auth)

── Booking API (all actions need token) ─────
GET    /restaurant/booking/                → List all bookings
POST   /restaurant/booking/                → Create booking
       Body: { "name": "John Doe", "no_of_guests": 4,
               "booking_date": "2025-06-20T19:00:00Z" }

GET    /restaurant/booking/<id>/           → Retrieve booking
PUT    /restaurant/booking/<id>/           → Full update
PATCH  /restaurant/booking/<id>/           → Partial update
DELETE /restaurant/booking/<id>/           → Delete

── Users ────────────────────────────────────
GET  /restaurant/users/                    → List users (auth)
GET  /restaurant/users/me/                 → Current user (auth)

── Admin ────────────────────────────────────
GET  /admin/                               → Django admin panel

AUTHENTICATION HEADER FORMAT
-----------------------------
Authorization: Token <your_auth_token_here>

RUNNING UNIT TESTS
------------------
USE_SQLITE=1 python manage.py test restaurant -v 2
