FROM python:3.6

# General workdir folder
WORKDIR /usr/app/src

# App requirements folder
RUN mkdir /usr/app/requirements/

# Installing app requirements using pip
ADD requirements/base.txt /usr/app/requirements/base.txt
RUN pip install --no-cache-dir -r /usr/app/requirements/base.txt
