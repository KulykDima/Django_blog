FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY healthcheck.sh /usr/src/healthcheck.sh
RUN chmod 0777 /usr/src/healthcheck.sh