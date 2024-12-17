FROM python:3.10.2-slim-buster

WORKDIR /app

COPY requirments.txt .

RUN pip3 install -r requirments.txt 

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python","server.py" ]