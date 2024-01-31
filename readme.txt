THis is dockerized container. Please use following commands in startup.sh to setup. Prereqsites:

Python, Docker, Postgres-12

This is a multi tire server architecture implementation for chat groups.

To see the implementation, first create env files:
.env.dev # Main Server
.env_africa.dev #Secondary servers
.env_china.dev
.env_eu.dev
.env_us.dev
.env_ind.dev

to generate coverage report as there are 2 servers, copy .env to main_server/groups_backend
and sec_server/groups_backend.

first create virtual env
ex: python -m venv venv
activate venv
source venv\bin\activate
install requirements:
pip install -r requirements.txt

then run 
coverage run manage.py test 
and 
coverage html 
in directories:
./sec_server and ./main_server

documentation is in docs directory and coverage report in coverage directory