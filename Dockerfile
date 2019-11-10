FROM python:3

LABEL maintainer="Cavour Poon <cavouriypoon@lionrockws.com>"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]