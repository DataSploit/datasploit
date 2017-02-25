FROM python:2-onbuild
MAINTAINER Brian Bustin <brian@bustin.us>

EXPOSE 8000
WORKDIR /usr/src/app/core
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]