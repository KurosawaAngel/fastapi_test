FROM python:3.12-slim

WORKDIR /app

RUN apt-get update &&\
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

CMD [ "fastapi", "run", "fastapi_test/main.py", "--port", "8000" ]