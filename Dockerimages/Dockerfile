FROM debian:jessie-slim
MAINTAINER Paul Ganea <k4ch0w@linux.com>
ENV C_FORCE_ROOT=root
RUN apt-get update -y && apt-get install -y  build-essential \
    curl \
    git \
    gnupg \
    libxml2-dev \
    libxmlsec1-dev \
    python \
    python-dev \
    runit \
    unzip \
    vim \
    wget \
    zip \
    && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6 \
    && echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list \
    && wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add - \
    && echo 'deb http://www.rabbitmq.com/debian/ testing main' || tee /etc/apt/sources.list.d/rabbitmq.list && apt-get update -y \
    && apt-get install -y mongodb-org rabbitmq-server  \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    && apt-get install -y libxml2-dev python-dev libxmlsec1-dev\
    && git clone https://github.com/DataSploit/datasploit \
    && cd datasploit \
    && mkdir /datasploit/datasploitDb  \
    && pip install -r requirements.txt \
    && useradd -ms /bin/bash k4ch0w \
    && apt-get remove -y libxml2-dev python-dev libxmlsec1-dev curl wget build-essential \
    && rm -rf /var/lib/apt/lists/*

USER k4ch0w
WORKDIR /datasploit
COPY service /etc/service/
COPY config.py /datasploit/config.py
ENTRYPOINT ["runsvdir", "/etc/service"]
