# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Рабочая директория
ENV APP_ROOT=/app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Переменная окружения для uv
# Указывает uv, что надо использовать эту директорию для
# сохранения файлов виртуального окружения

# Для старого pipenv
# ENV WORKON_HOME=/venv
ENV UV_PROJECT_ENVIRONMENT=/venv

RUN apt-get update && apt-get install -y --no-install-recommends bash

# Обновление pip и установка uv
RUN pip install --upgrade pip --no-cache-dir
RUN pip install uv --no-cache-dir


# Промежуточный образ для сборки
# Примерная экономия в размере образа ~ 70Mb
FROM base AS build

WORKDIR ${APP_ROOT}

# COPY ./services/fastapi/Pipfile ${APP_ROOT}
# COPY ./services/fastapi/Pipfile.lock ${APP_ROOT}
COPY ./services/fastapi/pyproject.toml ${APP_ROOT}
COPY ./services/fastapi/uv.lock ${APP_ROOT}

RUN uv sync --dev
RUN uv cache clean


# Итоговый образ
FROM base

COPY --from=build ${UV_PROJECT_ENVIRONMENT} ${UV_PROJECT_ENVIRONMENT}
WORKDIR ${APP_ROOT}

# Для продакшн
# COPY ./backend ${APP_ROOT}

# RUN uv run gunicorn 'hh.wsgi' --bind=0.0.0.0:8000