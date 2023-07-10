FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./mmello.com /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D caio
RUN chow -R caio:caio/vol
RUN chmod -R 755 /vol/web
USER caio

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["entrypoint.sh","gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
