# UksHub

UksHub is web based VCS, project management and collaboration tool. GitHub's twin brother.

## Available on Docker Hub

![example workflow](https://github.com/djolewalker/UksHub/actions/workflows/django.yml/badge.svg) ![example workflow](https://github.com/djolewalker/UksHub/actions/workflows/docker-hub.yml/badge.svg)

```
docker pull djolewalker/ukshub
```

## Team 3

| Contributor                                   | Full name                | Student Id |
| --------------------------------------------- | ------------------------ | ---------- |
| [erosdavid](https://github.com/erosdavid)     | David Ereš               | R2 36/2021 |
| [JSTheGreat](https://github.com/JSTheGreat)   | Jovan Svorcan            | R2 21/2021 |
| [djolewalker](https://github.com/djolewalker) | Dimitrije Žarković Đolai | R2 17/2021 |

## Setup:

### Clone repo:

```
git clone https://github.com/djolewalker/UksHub.git
cd UksHub
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

## Git server

Git server is implemented with Gitolite. Clone repo is also available through http and git protocols.

```
# Upload your public key trough application to be able to work with repo via SSH protocol
git clone ssh://git@127.0.0.1:2222/{user}/{repo-name}.git

# Http and git protocols
git clone http://127.0.0.1:8083/{user}/{repo-name}.git
git clone git://127.0.0.1:9418/{user}/{repo-name}.git
```

### To work with app locally do next:

1. Create bare repository locally on your pc
   ```
   mkdir git-admin-dev
   cd git-admin-dev
   git init --bare
   ```
2. Set GIT_ADMIN_REMOTE to bare admin repository absolute path in django dev settings
   ```
   ...
   GIT_ADMIN_REMOTE = "D:\git-admin-dev"
   ...
   ```
3. Clone repo to project
   ```
   git clone D:\git-admin-dev
   ```
4. Create initial file structure

   ```
   cd git-admin-dev

   mkdir conf
   cd conf
   echo > gitolite.conf

   # go back to git-admin-dev folder
   cd ..
   mkdir keydir
   echo > example.pub
   ```

5. Push initial setup to repo
   ```
   git add *
   git commit -m "Initial setup"
   git push
   ```

### Important for git server!!!

Clear previous volume with ssh key before another `docker-compose up` call

```
.\scripts\clear-ssh-volume.sh
docker-compose up --build
```
