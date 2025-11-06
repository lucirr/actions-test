FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /workspace

# 시스템 패키지
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY models/ ./models/
COPY pipelines/ ./pipelines/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY tests/ ./tests/

# Python path 설정
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# 기본 작업 디렉토리
WORKDIR /workspace