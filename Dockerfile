FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# 시스템 패키지 설치
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
COPY serving/ ./serving/
COPY data/ ./data/
COPY config/ ./config/

# 환경 변수
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI=http://mlflow-server.mlflow.svc.cluster.local:5000

# 기본 커맨드
CMD ["python", "models/train.py", "--config", "config/training_config.yaml"]