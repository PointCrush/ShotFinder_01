FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY work_dir /work_dir
WORKDIR /work_dir
EXPOSE 8000


RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "data_dir.asgi:application"]
