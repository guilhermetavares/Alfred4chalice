# This instruction sets the Python image at runtime
FROM python:3.8.11-slim-buster

# It ensures that the Python output is set straight to
# the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# necessary to work the file ./wait-for to use at command for api container.
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libcurl4-openssl-dev \
    default-libmysqlclient-dev \
    libssl-dev \
    netcat

# Creates ssh directory to save the ssh keys
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts

# Upgrade pip if necessary
RUN pip install --upgrade pip

COPY . /code/

# Install packages that help in development
COPY ./requirements/dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt

# Install any needed packages to run the tests
COPY ./requirements/test.txt /tmp/requirements-test.txt
RUN pip install -r /tmp/requirements-test.txt

WORKDIR /code/

# # Adds our working directory to the Python path
# ENV PYTHONPATH "${PYTHONPATH}:/var/task:/var/task/wallet"
