FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

LABEL maintainer="Kerem Ege Şahin <valvevaluejedi@gmail.com>"

RUN pip install -r requirements.txt

COPY ./src /src
