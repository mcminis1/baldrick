# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

RUN apt-get update; apt-get install -y cmake build-essential pkg-config libgoogle-perftools-dev git; rm -rf /var/lib/apt/lists/*;

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

RUN cd data;  python load_data_example.py; cd ..;

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 --preload src.app:api