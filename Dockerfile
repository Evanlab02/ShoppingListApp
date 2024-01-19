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
COPY shoppingapp /build/shoppingapp
COPY authentication /build/authentication
COPY stores /build/stores

RUN python -m build

FROM python:3.11.6-slim AS app

RUN apt-get update \
    && apt-get install make -y \
    && apt-get clean

RUN pip install pipenv

COPY manage.py /app/manage.py
COPY setup.py /app/setup.py
COPY pyproject.toml /app/pyproject.toml
COPY MANIFEST.in /app/MANIFEST.in
COPY version.txt /app/version.txt
COPY requirements.txt /app/requirements.txt
COPY version.txt /app/version.txt
COPY shoppingapp /app/shoppingapp
COPY authentication /app/authentication
COPY stores /app/stores

COPY --from=wheel-builder /build/dist /app/dist

WORKDIR /app

RUN pip install dist/*.whl
RUN rm -rf dist

EXPOSE 8000

CMD ["shoppingapp"]