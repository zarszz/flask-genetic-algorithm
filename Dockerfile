FROM python:alpine3.8

RUN apk update
RUN apk add python3-dev musl-dev

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]