FROM python:3.11.4-alpine3.18

WORKDIR /usr/src/

COPY ./ ./

RUN ls ./

RUN apk add build-base openjdk11

ENTRYPOINT [ "python", "reverie.py" ]
