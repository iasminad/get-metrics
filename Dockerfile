FROM ubuntu:22.04 

WORKDIR /metric_service

COPY metric_service/requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r requirements.txt

COPY metric_service /metric_service

ENV FLASK_APP=api.service

EXPOSE 8000 9090
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]
