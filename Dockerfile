FROM python:3

WORKDIR /.

COPY ./pyproject.toml /.

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .
