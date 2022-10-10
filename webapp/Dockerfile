FROM python:3.7

WORKDIR /app

COPY ./app/ /app
# COPY ./app/templates /app/templates

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "wallet_server.py"]