FROM registry.access.redhat.com/ubi9/python-311:latest

ENV DOWNLOAD_CACHE_LOCATION=/tmp

COPY requirements.txt /tmp/requirements.txt

USER root

RUN mkdir -p /app && \
    adduser default-user && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ADD src/ /app/

RUN chown -R default-user /app && \
    chmod -R 701 /app

USER default-user

WORKDIR /app

CMD ["python","main.py"]