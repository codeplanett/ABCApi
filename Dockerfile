FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

LABEL maintainer="Kerem Ege Şahin <valvevaluejedi@gmail.com>"

COPY . .

ENV CFLAGS=-Qunused-arguments
ENV CPPFLAGS=-Qunused-arguments
CMD sudo sed -i '.old' 's/ -m\(no-\)\{0,1\}fused-madd //g' /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/_sysconfigdata.py
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt
