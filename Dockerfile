FROM python:3.6.5

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/its

# https://pngquant.org/install.html
RUN cd $(mktemp -d) \
  && git clone --recursive https://github.com/kornelski/pngquant.git \
  && cd pngquant \
  && make install

RUN pip install pipenv
RUN pipenv --three
COPY Pipfile Pipfile.lock /opt/its/
RUN pipenv install --dev
COPY tox.ini /opt/its/
COPY its/ /opt/its/
