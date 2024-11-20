FROM xserrat/facebook-demucs:latest
WORKDIR /server

COPY requirment.txt /server/
COPY worker-server.py /server/

RUN pip3 install -r requirment.txt

ENTRYPOINT ["python3", "worker-server.py"]