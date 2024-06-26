# Test task backend for Precoro

This is a test task for the python developer position at Precoro.
Backend is implemented using Django Rest Framework.
After cloning the project you need to run next commands:

    python -m venv venv 
    source venv/bin/activate (for linux)
    venv\Scripts\activate (for windows)
    pip install -r requirements.txt
    cd shop
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata api/fixtures.json
    python manage.py runserver

The server will start at http://localhost:8000/

To see the list of endpoint you can go to http://localhost:8000/docs/swagger-ui/
