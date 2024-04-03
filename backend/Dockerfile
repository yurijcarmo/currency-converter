FROM python:3.11.4-alpine

RUN apk update && \
    apk add bash && \
    apk add --no-cache bash

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN python -m venv env
RUN /bin/bash -c "source env/bin/activate"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]