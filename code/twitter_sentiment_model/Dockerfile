FROM python:3.8

COPY app /app
COPY build/requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /app/data

WORKDIR /app
CMD ["python3", "main.py"]
