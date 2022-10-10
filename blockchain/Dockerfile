FROM python:3.7

WORKDIR /app

COPY ./app/ /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "blockchain_server.py"]