FROM kooplex-base
RUN   apt-get update
RUN  apt-get install python3 python3-pip -y
RUN  pip3 install --upgrade pip
RUN  pip3 install --upgrade GitPython   
RUN  pip3 install --upgrade django
RUN  pip3 install --upgrade ldap3
RUN  pip3 install --upgrade pymysql
RUN  pip3 install --upgrade docker-py django-threadlocals

ENV MYSQL_USER=mysql \
    MYSQL_DATA_DIR=/var/lib/mysql \
    MYSQL_RUN_DIR=/run/mysqld \
    MYSQL_LOG_DIR=/var/log/mysql

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server
