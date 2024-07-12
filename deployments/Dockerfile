FROM  python:3.7-alpine AS builder
EXPOSE 8000
WORKDIR /app 
COPY . /app/
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app 

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]