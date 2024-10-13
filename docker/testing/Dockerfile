FROM python:3.12.4-alpine3.20

RUN apk add --no-cache bash build-base gcc python3-dev musl-dev linux-headers
COPY testing/requirements.txt /install/requirements.txt

WORKDIR /install/
RUN pip install -r requirements.txt

WORKDIR /server
COPY testing/ /server
CMD ["locust", "-f", "__init__.py", "--processes", "4", "--exclude-tags", "auth", "api"]
