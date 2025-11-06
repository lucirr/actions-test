# kubeflow pipeline
from kfp import Client
from kfp import dsl
from kfp.compiler import Compiler

KFP_ENDPOINT = "http://KUBEFLOW_URL/pipeline"

# Kubeflow Pipeline 정의
@dsl.pipeline(
    name="ML Train Pipeline",
    description="Train, evaluate, and register model"
)
def train_pipeline(image: str, model_name: str):

    # Training step
    train = dsl.ContainerOp(
        name="train",
        image=image,
        command=["python", "model/train.py"]
    )

    # Evaluation step
    evaluate = dsl.ContainerOp(
        name="evaluate",
        image=image,
        command=["python", "model/evaluate.py"],
    )

    # MLflow 모델 등록
    register = dsl.ContainerOp(
        name="register_to_mlflow",
        image=image,
        command=["python", "model/register.py"],
        arguments=["--model-name", model_name]
    )

    # 의존성 연결
    train >> evaluate >> register


# Pipeline 실행 함수 (파일 없이 실행)
def run_pipeline(image: str, model_name: str):
    client = Client(host=KFP_ENDPOINT)

    # pipeline.yaml 생성 없이 바로 실행
    run = client.create_run_from_pipeline_func(
        train_pipeline,
        arguments={
            "image": image,
            "model_name": model_name
        }
    )

    print(f" Kubeflow Pipeline triggered!")
    print(f"   run id: {run.run_id}")


# CLI 실행 가능하도록
if __name__ == "__main__":
    import sys
    image = sys.argv[1]   # ex: my-registry/my-model:sha256
    model_name = "my-demo-model"

    run_pipeline(image, model_name)

