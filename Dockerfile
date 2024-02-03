FROM python:3.11.6-slim AS wheel-builder

WORKDIR /build

COPY requirements.txt /build/requirements.txt
RUN pip install -r requirements.txt
RUN pip install build

COPY manage.py /build/manage.py
COPY setup.py /build/setup.py
COPY pyproject.toml /build/pyproject.toml
COPY MANIFEST.in /build/MANIFEST.in
COPY version.txt /build/version.txt
COPY authentication /build/authentication
COPY stores /build/stores
COPY shoppingapp /build/shoppingapp

RUN python -m build

FROM python:3.11.6-slim AS app

RUN apt-get update \
    && apt-get install make -y \
    && apt-get clean

RUN pip install pipenv

COPY --from=wheel-builder /build/ /app/

WORKDIR /app

RUN pip install dist/*.whl
RUN rm -rf dist

EXPOSE 8000

CMD ["shoppingapp"]