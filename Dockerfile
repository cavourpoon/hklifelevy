FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./* /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]