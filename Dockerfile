# pull official base image
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
#directory to store app source code
RUN mkdir -p /src/app and chown 777 /src/app
WORKDIR /src/app

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /src/app/
RUN pip install -r requirements.txt

# copy project
COPY . .