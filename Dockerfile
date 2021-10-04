FROM python:3.6-alpine

RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

RUN apk update && \
    apk upgrade && \
    apk add gcc && \
    apk add g++ && \
    apk add make && \
    apk add postgresql-libs && \
    apk add sqlite && \
    apk add musl-dev && \
    apk add zlib-dev && \
    apk add postgresql-dev && \
    apk add libxml2-dev && \
    apk add libxslt-dev && \
    apk add bash && \
    mkdir -p /src/db && \
    mkdir -p /tmp

COPY requirements.txt /src/source/requirements.txt
RUN pip install -r /src/source/requirements.txt

COPY . /src/source

WORKDIR /src/source
EXPOSE 8000
ENV PYTHONPATH /src/source
#CMD ["python", "/src/source/main.py"]
ENTRYPOINT ["gunicorn", "--config", "/src/source/config.py", "main:application"]