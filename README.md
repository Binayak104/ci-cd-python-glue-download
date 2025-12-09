# CI/CD Python Glue Demo (us-east-1)

This repo shows a production-style pattern where Python glues together CI/CD steps:

- Run tests via `subprocess`.
- Build and push a Docker image to Amazon ECR.
- Trigger an external deploy system (e.g., Jenkins) via HTTP `requests`.
- All infrastructure (ECR) is provisioned using Terraform in `us-east-1`.

## 1. Terraform: provision ECR (us-east-1)

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

Output:
- `ecr_repository_url` – ECR repo URL.
- `ecr_repository_name` – repo name (used by CI).

## 2. Local dev (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run tests
python -m ci_tools.run_tests

# build & push image (requires AWS CLI login to ECR)
python -m ci_tools.build_and_push_image
```

Required env vars when pushing locally:

- `ECR_REGISTRY` (e.g. `123456789012.dkr.ecr.us-east-1.amazonaws.com`)
- `ECR_REPOSITORY` (e.g. `ci-glue-demo-repo`)
- `IMAGE_TAG` (default: `latest`)

## 3. GitHub Actions CI/CD

1. Push this repo to GitHub.
2. Configure repository secrets:

   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - (optional) `JENKINS_URL`, `JENKINS_USER`, `JENKINS_API_TOKEN` for deploy.

3. Update `ECR_REPOSITORY` in `.github/workflows/ci-cd.yml` to match the Terraform output if needed.

On push to `main`, the pipeline will:

- Install Python deps.
- Run tests.
- Login to ECR.
- Build and push Docker image tagged with the commit SHA.
- Optionally trigger external deploy (Jenkins) via Python + `requests`.
