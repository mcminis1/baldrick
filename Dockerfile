# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# sentence transformers has some packages that must be built.
RUN apt-get update; apt-get install -y cmake build-essential pkg-config libgoogle-perftools-dev git; rm -rf /var/lib/apt/lists/*;
RUN pip install torch torchvision sentencepiece --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install sentence-transformers==1.1.0

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy download script over
COPY src/data/download_models.py src/data/download_models.py

# download the encodings stuff.
RUN python src/data/download_models.py

# Copy the rest of the code over (for caching efficiency)
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 --preload src.app:api