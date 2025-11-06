# Kubeflow Pipeline 트리거 스크립트
from kfp import Client
from kfp.compiler import Compiler
from pipelines.train_pipeline import train_pipeline

def run_pipeline(image_tag: str, model_name: str):
  client = Client(host="http://KUBEFLOW_ENDPOINT")

  # pipeline.yaml을 직접 저장하지 않고 메모리에서 컴파일
  pipeline_package = Compiler().compile(train_pipeline)

  run = client.create_run_from_pipeline_func(
      train_pipeline,
      arguments={ "image": image_tag, "model_name": model_name }
  )

  print("Kubeflow pipeline started")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        exit(1)

    image_tag = sys.argv[1]
    model_name = sys.argv[2]
    run_pipeline(image_tag, model_name)
