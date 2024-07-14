FROM  python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /app 
COPY requirements/prod.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY ./app /app 

COPY deployments/deploy.sh /etc/app/deploy.sh

ENTRYPOINT ["sh", "/etc/app/deploy.sh"]