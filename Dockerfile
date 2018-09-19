FROM python:3.5

ENV PYTHONUNBUFFERED 1

WORKDIR /srv/tube

ENTRYPOINT ["docker/entrypoint.sh"]

ADD requirements.txt /srv/tube/requirements.txt

RUN pip install -r requirements.txt

COPY . .
