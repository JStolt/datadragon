# Dockerfile - postgres alpine base image with CSV data load

FROM postgres:14.2-alpine

RUN apk update
RUN apk upgrade
# RUN apk install wget

RUN mkdir /data

RUN wget -O /usr/local/bin/pgfutter https://github.com/lukasmartinelli/pgfutter/releases/download/v1.2/pgfutter_linux_amd64
RUN chmod +x /usr/local/bin/pgfutter

# RUN /etc/init.d

RUN psql -U postgres -c 'create databse sample;'

CMD pgfutter --db_name sample /data/*.csv



#docker build -f $PWD/sandbox/postgres/Dockerfile -t datadragon_pg:0.1
#docker run --rm -it -v $PWD/sandbox/data/csv:/data -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres


