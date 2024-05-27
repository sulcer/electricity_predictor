ARG PYTHON_VERSION=3.12.2
ARG PORT=8000

FROM python:${PYTHON_VERSION}  as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN pip install --upgrade pip setuptools wheel

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:${PYTHON_VERSION} as runner

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libhdf5-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "src.serve.main:app", "--host", "0.0.0.0", "--port", "8000"]