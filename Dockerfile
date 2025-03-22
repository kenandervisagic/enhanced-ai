FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir /app/output

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
