import subprocess
import sys

def main() -> None:
    """Run test suite using pytest via subprocess for full control/logging."""
    cmd = [sys.executable, "-m", "pytest", "-q"]
    print(f"Running tests: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Tests failed with exit code {exc.returncode}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()
