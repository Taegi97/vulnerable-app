# 오래된 버전의 Python 이미지를 사용하여 Trivy가 취약점을 찾도록 유도합니다.
FROM python:3.8-slim-buster

WORKDIR /app
COPY app.py .
RUN pip install Flask==1.1.2

CMD ["python", "app.py"]
