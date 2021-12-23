# uks-hub

Uks-hub is web based VCS, project management and collaboration tool. GitHub's twin brother.

## Team 3
| Contributor | Full name | Student Id |
| ------ | ------ | ------ |
| [erosdavid](https://github.com/erosdavid) |  David Ereš | R2 36/2021 | 
| [JSTheGreat](https://github.com/JSTheGreat) | Jovan Svorcan | R2 21/2021 | 
| [djolewalker](https://github.com/djolewalker) | Dimitrije Žarković Đolai | R2 17/2021 |

## Setup:
### Clone repo:
```python
git clone https://github.com/djolewalker/UksHub.git
cd uks-hub
```
### Create venv:
```python
# Install venv if you don't have it
pip install venv

# Create virtual environment
python venv venv

# Start virtual environment 
.\venv\Scripts\activate
```
### Run locally:
You will need MySQL server (e.g. [WAMP](https://www.wampserver.com/en/)). 
When you have MySql running on your device execute scripts/create_db_local.sql script.
When database is ready we can migrate data.
```python
# Migrate data
(venv)> pip install -r requirements.txt
(venv)> python manage.py makemigrations
(venv)> python manage.py migrate
```
Run server with next command:
```python
(venv)> python manage.py runserver
```
App will be running on django's default port [http://localhost:8000/](http://localhost:8000/)

### Run with docker:
You will need docker installed on your machine.
```python
# Run docker compose from root folder (ukshub) to run docker file
# Be patient first time
docker-compose up --build
```
```python
# Follow instructions in docker-compose.yml file to run container from image on DockerHub 
# Run docker compose with --force-recreate parameter to rebuild container from remote image
docker-compose up --build --force-recreate
```
App will be running on [http://localhost:8083/](http://localhost:8083/)
