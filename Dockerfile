# base image
FROM python:3.9

#maintainer
LABEL Author="Luis Mex"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV DJANGO_SETTINGS_MODULE encuentas_whats.settings
#directory to store app source code
RUN mkdir /code

#switch to /app directory so that everything runs from here
WORKDIR /code

#copy the app code to image working directory
COPY ./requirements.txt /code

RUN apt-get update && apt-get upgrade -y && apt-get install mariadb-server mariadb-client  -y

#let pip install required packages
RUN pip install -r requirements.txt
COPY . /code
RUN python manage.py collectstatic --no-input