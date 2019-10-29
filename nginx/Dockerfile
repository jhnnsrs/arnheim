FROM alpine:3.6
ENV NGINX_VERSION 1.13.6

# Workaround for weird windows line bug
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted
COPY install.sh /usr/src/
RUN dos2unix /usr/src/install.sh

COPY nginx.key /usr/src/
RUN sh -x /usr/src/install.sh

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.vh.default.conf /etc/nginx/conf.d/default.conf

# Create hashed temporary upload locations
RUN mkdir -p /media/_upload/0 && \
    mkdir -p /media/_upload/1 && \
    mkdir -p /media/_upload/2 && \
    mkdir -p /media/_upload/3 && \
    mkdir -p /media/_upload/4 && \
    mkdir -p /media/_upload/5 && \
    mkdir -p /media/_upload/6 && \
    mkdir -p /media/_upload/7 && \
    mkdir -p /media/_upload/8 && \
    mkdir -p /media/_upload/9 && \
    chmod 777 -R /media/_upload

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
