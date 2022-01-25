release: python3 manage.py compress --force && python3 manage.py collectstatic --noinput
web: gunicorn --workers=3 UksHub.wsgi