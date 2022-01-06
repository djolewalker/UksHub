# uncomment this to use sqlite as test db
#export UKS_TEST_DB=ON
# collect static files and put inside ./static/
python3 manage.py collectstatic --noinput
python3 manage.py compress --force
# setup db
python3 manage.py makemigrations
python3 manage.py migrate
# python3 manage.py db_script
# run Django develop server
# python3 manage.py runserver 0.0.0.0:8000
# run Django app inside gunicorn
# always use more than 1 worker
gunicorn --workers=3 UksHub.wsgi -b 0.0.0.0:8000