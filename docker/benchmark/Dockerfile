FROM python:3.13.2-alpine3.21

ENV UV_SYSTEM_PYTHON 1

RUN apk add --no-cache bash build-base gcc linux-headers musl-dev python3-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY benchmark/requirements.txt /app/requirements.txt

WORKDIR /app
RUN uv pip install -r requirements.txt

WORKDIR /app
COPY benchmark/ /app
ENTRYPOINT [ "locust" ]
CMD [ "-f", "__init__.py", "--processes", "2", "--tags", "api" ]
