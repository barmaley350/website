# syntax=docker/dockerfile:1

FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./services/nginx/nginx.conf /etc/nginx/conf.d

# RUN chown -R nginx:nginx /usr/share/nginx/html