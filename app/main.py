import os
from datetime import datetime

def main() -> None:
    app_name = os.getenv("APP_NAME", "ci-glue-demo")
    now = datetime.utcnow().isoformat()
    print(f"[{now}] Hello from {app_name}! CI/CD glue is working.")

if __name__ == "__main__":
    main()
