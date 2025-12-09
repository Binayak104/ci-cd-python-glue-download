import os
import subprocess
import sys
from typing import Optional

def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main() -> None:
    """Build and push Docker image to ECR using docker CLI + subprocess.

    Expects environment variables:

    - ECR_REGISTRY   e.g. 123456789012.dkr.ecr.us-east-1.amazonaws.com
    - ECR_REPOSITORY e.g. ci-glue-demo-repo
    - IMAGE_TAG      e.g. a commit SHA (default: 'latest')
    """
    registry = os.getenv("ECR_REGISTRY")
    repository = os.getenv("ECR_REPOSITORY")
    tag = os.getenv("IMAGE_TAG", "latest")

    if not registry or not repository:
        print("ECR_REGISTRY and ECR_REPOSITORY must be set in env.", file=sys.stderr)
        sys.exit(1)

    local_image = f"{repository}:{tag}"
    remote_image = f"{registry}/{repository}:{tag}"

    print(f"Building local image: {local_image}")
    _run(["docker", "build", "-t", local_image, "."])

    print(f"Tagging {local_image} as {remote_image}")
    _run(["docker", "tag", local_image, remote_image])

    print(f"Pushing {remote_image}")
    _run(["docker", "push", remote_image])

    print("Image pushed successfully.")

if __name__ == "__main__":
    main()
