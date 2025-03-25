FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/output

RUN mkdir /app/output/audio

RUN mkdir /app/output/images

RUN mkdir /app/output/story

RUN mkdir /app/output/video

RUN mkdir /app/output/love_videos

RUN mkdir /app/output/quotes

COPY app/ .

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
