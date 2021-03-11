FROM ubuntu:18.04

ENV TZ=US
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt update \
    && apt install software-properties-common -y \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get install libpq-dev gcc python3-dev python3-venv -y \
    && useradd -ms /bin/bash api \
    && apt-get clean

WORKDIR /home/api

COPY app app
COPY requirements.txt requirements.txt
COPY travel.py boot.sh ./

ENV FLASK_APP travel.py

RUN chmod +x boot.sh \
    && python3 -m venv venv \
    && venv/bin/pip install --upgrade pip \
    && venv/bin/pip install -r requirements.txt \
    && venv/bin/pip install gunicorn \
    && chown -R api:api ./

USER api

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]



