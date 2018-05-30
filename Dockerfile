FROM python:3.6.5

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/its

RUN apt-get update && apt-get install -y \
    pngquant \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv
RUN pipenv --three
COPY Pipfile Pipfile.lock /opt/its/
RUN pipenv install --dev
COPY tox.ini /opt/its/
COPY its/ /opt/its/
