## Little Lemon Restaurant – Back-End Capstone Project

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

