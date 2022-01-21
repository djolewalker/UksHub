FROM python:3
ENV PYTHONUNBUFFERED 1

# setup working directory
RUN mkdir /code
WORKDIR /code
ADD . /code

# Sometimes, some prerequisites are needed for psycopg2
# See for more (https://stackoverflow.com/questions/16629081/cant-install-psycopg2)

RUN pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY /config/web/.gitconfig /etc/gitconfig
COPY /config/web/ssh_config /etc/ssh/ssh_config

# make these scripts executables
RUN ["chmod", "+x", "./scripts/create-public-key.sh"]
RUN ["chmod", "+x", "./scripts/wait_for_mysql.sh"]
RUN ["chmod", "+x", "./scripts/start-django.sh"]