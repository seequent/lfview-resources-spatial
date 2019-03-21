FROM python:3.6
MAINTAINER "Franklin Koch <franklin.koch@seequent.com>"

RUN apt-get update && apt-get -y install vim
RUN apt-get -y install graphviz

# Make the destination directory
RUN mkdir -p /usr/src/app/docs
WORKDIR /usr/src/app

# Copy resources
COPY docs/scripts docs/templates docs/conf.py docs/Makefile /usr/src/app/docs/
COPY setup.py requirements.txt requirements_dev.txt Makefile README.rst /usr/src/app/

# Install requirements
RUN pip install -r requirements_dev.txt

COPY lfview /usr/src/app/lfview
