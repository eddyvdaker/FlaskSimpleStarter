FROM python:3.8.2-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app

RUN python manage.py db downgrade
RUN python manage.py db upgrade
RUN python manage.py seed-db

CMD ["/usr/src/app/entrypoint.sh"]