FROM python:3.11.1-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

ENV PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install redis

COPY venue_preparation.csv venue_preparation.csv
COPY insert_venue_preparation.py insert_venue_preparation.py

