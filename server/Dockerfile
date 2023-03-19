FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

RUN apt-get update

RUN pip install --upgrade pip

COPY . $DockerHOME

RUN pip3 install -r requirements.txt