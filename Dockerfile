# We need to start from a copy of the python:3.7-alpine image published to our private registry since the list of
# available images on the CloudBees Jenkins servers does not include python:3-alpine.

#FROM artifactory.cms.gov/bedap-docker-local/python:3.7-alpine-pipenv
FROM python:3.7-slim

# Install parameter-store-exec, which fetches secrets from AWS SSM
# and sets them as environment variables
# (see https://github.com/cultureamp/parameter-store-exec)
COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock

RUN pip3 install pipenv
RUN pip install --upgrade pip
RUN set -ex && pipenv install --deploy --system


COPY ./app   ./
COPY ./crt/server.key /var/lib/postgresql/server.key
COPY ./crt/server.crt /var/lib/postgresql/server.crt

CMD ["python", "-u", "main.py", "run"]