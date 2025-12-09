import os
import sys
import requests

def main() -> None:
    """Trigger an external deploy system (e.g., Jenkins) via HTTP.

    Expects env vars:

    - JENKINS_URL        e.g. https://jenkins.company/job/prod/build
    - JENKINS_USER
    - JENKINS_API_TOKEN
    """
    url = os.getenv("JENKINS_URL")
    user = os.getenv("JENKINS_USER")
    token = os.getenv("JENKINS_API_TOKEN")

    if not url or not user or not token:
        print("JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN must be set.", file=sys.stderr)
        sys.exit(1)

    print(f"Triggering deploy via {url}")
    resp = requests.post(url, auth=(user, token))
    if resp.status_code >= 400:
        print(f"Deploy trigger failed: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    print("Deploy trigger accepted by Jenkins (or external system).")

if __name__ == "__main__":
    main()
