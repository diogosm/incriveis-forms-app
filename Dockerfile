FROM python:3.9-slim-buster

RUN apt-get update \
        && DEBIAN_FRONTEND=noninteractive; \
        apt-get install -y libaio1 wget unzip;

## lib pro git
## RUN apt-get -y install git

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

## @TODO
##	criar token de acesso pra esse git

#CMD ["python", "main.py"]
EXPOSE 5000
CMD ["gunicorn", "--workers=2", "--timeout=90", "--worker-class=gevent", "--threads=3", "--bind=0.0.0.0:5000", "main:app"]
