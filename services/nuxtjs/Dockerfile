# syntax=docker/dockerfile:1

FROM node:current-slim AS base
ENV APP_ROOT=/app
ENV NODE_ENV=development

WORKDIR ${APP_ROOT}

FROM base AS build

COPY ./services/nuxtjs/package-lock.json ${APP_ROOT}
COPY ./services/nuxtjs/package.json ${APP_ROOT}

RUN npm install

FROM base

COPY --from=build ${APP_ROOT}/node_modules ${APP_ROOT}/node_modules
