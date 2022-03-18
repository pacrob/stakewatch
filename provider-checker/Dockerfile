# syntax=docker/dockerfile:1

FROM python:3.9.10-buster

WORKDIR /provider-checker

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

