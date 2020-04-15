
From mysql:5.7

RUN apt-get update && apt-get install pv

WORKDIR /database/

RUN mkdir mysql-scripts

COPY ./get-staging-db.sh /database/get-staging-db.sh

COPY ./update-local-db.sh /database/update-local-db.sh

COPY ./.my.cnf /root/.my.cnf 

COPY ./mysql-scripts/ /docker-entrypoint-initdb.d/

