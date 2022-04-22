FROM postgres:14.2-bullseye

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

RUN pip --no-cache install pandas

RUN mkdir /data

COPY init-db.sh schema-gen.py /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

EXPOSE 5432