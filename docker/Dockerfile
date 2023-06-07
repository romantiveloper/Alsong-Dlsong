# pull official base image
FROM python:3.8.0-alpine


# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update
RUN apk add postgresql-dev mariadb-dev gcc python3-dev musl-dev zlib-dev jpeg-dev  #--(5.2)


COPY . /usr/src/app/
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]