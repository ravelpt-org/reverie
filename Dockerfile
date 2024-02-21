FROM python:3.11.4-alpine3.18

WORKDIR /usr/src/

COPY ./ ./

RUN ls ./

RUN apk add build-base
RUN apk --no-cache add openjdk11 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

ENTRYPOINT [ "python", "reverie.py" ]
