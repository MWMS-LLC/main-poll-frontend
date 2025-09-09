FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .

EXPOSE 8080

CMD ["python3", "main.py"]
