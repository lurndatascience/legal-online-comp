# syntax=docker/dockerfile:1
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/
ARG PYTHON_VERSION=3.11.4

FROM python:${PYTHON_VERSION}-slim as base
# Environment Variables
ENV BACKEND_API_PORT=3001
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Prevents Python from writing pyc files.
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
#ENV PYTHONUNBUFFERED=1

# Update and install necessary packages to fix vulnerabilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # openssl=3.0.11-1~deb12u2 \
    libc-bin=2.36-9+deb12u3 \
    libkrb5-3=1.20.1-2+deb12u1 \
    libgssapi-krb5-2=1.20.1-2+deb12u1 \
    libgnutls30=3.7.9-2+deb12u1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN useradd -m -u ${UID} appuser
RUN apt-get update && \
    apt-get install -y gcc musl-dev python3-dev libpq-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies with pipenv
# Assumes you have a Pipfile and Pipfile.lock in your project directory
COPY requirements.txt ./
# Cleaning, installing packages, and checking environment
# RUN pipenv install --system --deploy --verbose --clear

# TODO: Replace with above pipenv execution once the new Pipfile.lock has been generated
# Install CPU-version of torch first to keep image small (avoid installation of GPU version)
RUN python -m pip install --upgrade pip \ 
    && python -m pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu \
    && python -m pip install -r requirements.txt

#    && python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \

RUN mkdir -p /cache && chmod 777 /cache
ENV TRANSFORMERS_CACHE /cache
# RUN apt-get update && apt-get install -y libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* 
# Switch to the non-privileged user to run the application.
#USER appuser

# Copy the source code into the container
COPY . .
# # Converts online-component into a package
# RUN python -m pip install -e .

## For debugging and editing of the source code inside the container:
# Change ownership of /app to appuser
RUN mkdir -p /app/logs \
    && mkdir -p /app/data \
    && usermod -d /app appuser \    
    && chown -R appuser:appuser /app  \
    && chmod +x ./entrypoint.sh

USER appuser

# Expose the ports the application uses
EXPOSE 8888
EXPOSE 6060
EXPOSE $BACKEND_API_PORT

# # Do not run anything, just keep the Container alive.
# CMD tail -f /dev/null

CMD ["./entrypoint.sh"]
