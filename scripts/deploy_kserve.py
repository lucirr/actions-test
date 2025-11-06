#!/usr/bin/env python3
"""
KServe InferenceService 배포 스크립트
serving/kserve.yaml 템플릿의 변수를 치환하여 배포합니다.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from string import Template


def load_template(template_path: str) -> str:
    """YAML 템플릿 파일을 로드합니다."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def substitute_variables(template_content: str, model_version: str,
                         namespace: str, canary_percent: int) -> str:
    """템플릿의 변수를 실제 값으로 치환합니다."""
    template = Template(template_content)

    substituted = template.safe_substitute(
        namespace=namespace,
        modelVersion=model_version,
        canaryPercent=canary_percent
    )

    return substituted


def apply_kserve_config(yaml_content: str) -> bool:
    """kubectl apply를 사용하여 KServe 설정을 배포합니다."""
    try:
        process = subprocess.Popen(
            ['kubectl', 'apply', '-f', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(input=yaml_content)

        if process.returncode == 0:
            print("KServe InferenceService 배포 성공!")
            print(stdout)
            return True
        else:
            print("KServe InferenceService 배포 실패!")
            print(stderr)
            return False

    except FileNotFoundError:
        print("kubectl이 설치되어 있지 않습니다.")
        return False
    except Exception as e:
        print(f"배포 중 오류 발생: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='KServe InferenceService를 배포합니다.'
    )
    parser.add_argument(
        '--model-version',
        required=True,
        help='배포할 모델 버전 (예: v1.0.0)'
    )
    parser.add_argument(
        '--namespace',
        required=True,
        help='배포할 Kubernetes 네임스페이스 (예: production)'
    )
    parser.add_argument(
        '--canary-percent',
        type=int,
        default=10,
        help='카나리 배포 트래픽 비율 (기본값: 10)'
    )
    parser.add_argument(
        '--template-path',
        default='serving/kserve.yaml',
        help='KServe YAML 템플릿 파일 경로 (기본값: serving/kserve.yaml)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 배포 없이 생성될 YAML만 출력'
    )

    args = parser.parse_args()

    # 템플릿 파일 존재 확인
    template_path = Path(args.template_path)
    if not template_path.exists():
        print(f"템플릿 파일을 찾을 수 없습니다: {args.template_path}")
        sys.exit(1)

    print("KServe 배포 설정:")
    print(f"  - 모델 버전: {args.model_version}")
    print(f"  - 네임스페이스: {args.namespace}")
    print(f"  - 카나리 트래픽: {args.canary_percent}%")
    print(f"  - 템플릿 파일: {args.template_path}")
    print()

    # 템플릿 로드
    template_content = load_template(args.template_path)

    # 변수 치환
    yaml_content = substitute_variables(
        template_content,
        args.model_version,
        args.namespace,
        args.canary_percent
    )

    # KServe 배포
    print(" KServe InferenceService 배포 중...")
    success = apply_kserve_config(yaml_content)

    if success:
        print(f"   kubectl get inferenceservice -n {args.namespace}")
        print(f"   kubectl describe inferenceservice sklearn-iris -n {args.namespace}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
