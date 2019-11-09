FROM ubuntu:16.04

MAINTANER Your Name "youremail@domain.tld"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./* /app/requirements.txt

WORKDIR /app

RUN pip install

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]