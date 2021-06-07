#FROM artifactory.cms.gov/bedap-docker-local/python:3.7-alpine-pipenv
FROM python:3.9-slim

# Install parameter-store-exec, which fetches secrets from AWS SSM
# and sets them as environment variables
# (see https://github.com/cultureamp/parameter-store-exec)

COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock
COPY tempFile.pem ./tempFile.pem

RUN pip3 install pipenv
RUN pip install --upgrade pip
RUN set -ex && pipenv install --deploy --system

COPY ./main.py   ./main.py

CMD ["python", "-u", "main.py", "run"]