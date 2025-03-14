FROM python:3.12.8

WORKDIR /srv/

COPY . .

RUN pip install -r requirements.txt
