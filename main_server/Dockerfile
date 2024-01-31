# pull official base image
FROM python:3.8.10-buster

# set work directory
WORKDIR /main_server
RUN apt update

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .

