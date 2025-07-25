FROM python:3.10-slim

WORKDIR /metric_service

COPY metric_service/requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r requirements.txt

COPY metric_service /metric_service

EXPOSE 8000
