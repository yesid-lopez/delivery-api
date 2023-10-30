#-------------#
# Stage: base #
#-------------#

FROM python:3.11.1-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

ENV HOST=0.0.0.0

#----------------#
# Stage: builder #
#----------------#

FROM base as builder

ENV PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.0

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry export --without dev -f requirements.txt --without-hashes -o requirements-prod.txt
RUN poetry export --with dev -f requirements.txt --without-hashes -o requirements-dev.txt

#------------#
# Stage: dev #
#------------#

FROM base as dev

WORKDIR app

COPY --from=builder /requirements-dev.txt /app
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

#-------------#
# Stage: prod #
#-------------#

FROM base as prod

WORKDIR app
COPY delivery_api delivery_api
COPY --from=builder /requirements-prod.txt /app
RUN pip install --no-cache-dir -r /app/requirements-prod.txt

CMD python -m delivery_api