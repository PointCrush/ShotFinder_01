FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY work_dir /work_dir
WORKDIR /work_dir
EXPOSE 8000

#RUN apk update
#RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
