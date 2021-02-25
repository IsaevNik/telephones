FROM python:3.7

RUN pip3 install pipenv

WORKDIR /usr/src/telephones

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --system --deploy --ignore-pipfile

COPY . .

ENTRYPOINT ["python3.7", "telephone_parser.py"]
