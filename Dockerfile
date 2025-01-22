FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000

CMD ["python", "src/main.py"]