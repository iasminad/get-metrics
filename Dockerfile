FROM ubuntu:22.04

# Set working directory inside container
WORKDIR /metric_service

# Copy requirements.txt from host into container
COPY metric_service/requirements.txt .

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python3 -m pip install -r requirements.txt

# Copy the service.py into the container
COPY metric_service /metric_service
# COPY metric_service/api/service.py /metric_service/api/service.py
# COPY metric_service/api/templates /metric_service/api/templates
# COPY metric_service/client/agent.py /metric_service/client/agent.py
# COPY metric_service/server/collector.py /metric_service/server/collector.py

# Set environment variables for Flask
ENV FLASK_APP=api.service

# Expose Flask port
EXPOSE 8000
CMD ["flask", "run", "--port=8000", "--debug"]
