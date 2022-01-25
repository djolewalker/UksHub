release: python manage.py compress --force && python manage.py collectstatic --no-input
web: gunicorn --workers=3 UksHub.wsgi