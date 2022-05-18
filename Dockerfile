FROM python:3.9-alpine3.13
LABEL maintaner="guilhermefq"

# para não ter que esperar o buffer chegar ao python
ENV PYTHONBUNFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

# um unico comando para evitar a criação de camadas no container
RUN python -m venv /py && \
    apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache mariadb-dev && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del build-deps && \
    adduser \
      --disabled-password \
      --no-create-home \
      django-user

ENV PATH="/py/bin:$PATH"

USER django-user