FROM apache/superset:latest

USER root

# Install required dependencies and psycopg2-binary system-wide
RUN apt-get update && apt-get install -y gcc libpq-dev python3-dev \
    && pip install --no-cache-dir psycopg2-binary \
    && apt-get remove -y gcc python3-dev \
    && apt-get autoremove -y \
    && apt-get clean

USER superset











##FROM apache/superset:latest

##USER root

##RUN apt-get update && apt-get install -y gcc libpq-dev python3-dev \
    ##&& pip install --no-cache-dir psycopg2-binary \
    ##&& apt-get remove -y gcc python3-dev \
    ##&& apt-get autoremove -y \
    ##&& apt-get clean

##USER superset








##FROM apache/superset:latest

##USER root
##RUN pip install --no-cache-dir psycopg2-binary

##USER superset
