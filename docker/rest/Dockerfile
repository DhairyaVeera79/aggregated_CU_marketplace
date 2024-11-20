FROM python:3.8.2-alpine

WORKDIR /server

COPY requirments.txt /server/
COPY rest-server.py /server/

RUN pip3 install -r requirments.txt

ENTRYPOINT ["python", "rest-server.py"]