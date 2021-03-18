ARG PACKAGE_NAME=excerpt_formatter

FROM node:15.10.0-stretch
ARG PACKAGE_NAME
ADD ${PACKAGE_NAME}/frontend /
RUN yarn
RUN yarn build

FROM python:3.9.2-buster
ARG PACKAGE_NAME
RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn

# Copy Gunicorn configuration into image
ADD ./docker/gunicorn /
RUN chmod +x /start.sh
RUN chmod +x /start-reload.sh

RUN pip install --no-cache-dir fastapi

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

# Install project dependencies from pyproject.toml
COPY pyproject.toml poetry.lock* /
RUN poetry install --no-root --no-dev

# Copy node packages from intermediate node image into main Python image
COPY ./${PACKAGE_NAME}/frontend /app/frontend
COPY --from=0 /dist /app/frontend/dist

# Copy backend Python files to the main image
COPY ./${PACKAGE_NAME}/backend/app /app

EXPOSE 80

WORKDIR /app/
ENV PYTHONPATH=/app
CMD ["/start.sh"]
