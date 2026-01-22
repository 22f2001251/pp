import requests
import subprocess
from datetime import datetime, timezone

# ---------------- CONFIG ----------------
WEBSITES = {
    "airtel": "https://www.airtel.in",
    "jio": "https://www.jio.com",
    "phonepe": "https://www.phonepe.com",
    "flipkart": "https://www.flipkart.com",
    "paytm": "https://paytm.com"
}

# ---------------- UTILITY ----------------
def run(cmd):
    """
    Run a shell command.
    Raises error if command fails.
    """
    subprocess.run(cmd, shell=True, check=True)

# ---------------- FETCH HEADERS ----------------
def fetch_headers():
    """
    Fetch headers from websites and save to a new file.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"headers_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"FETCH TIME: {timestamp} UTC\n")
        f.write("=" * 50 + "\n")

        for name, url in WEBSITES.items():
            f.write(f"\n[{name.upper()}] {url}\n")
            try:
                r = requests.get(url, timeout=15)
                f.write(f"STATUS: {r.status_code}\n")
                for k, v in r.headers.items():
                    f.write(f"{k}: {v}\n")
            except Exception as e:
                f.write(f"ERROR: {e}\n")

    return filename

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Configure Git identity for this repo
    run('git config user.name "GitHub Actions Bot"')
    run('git config user.email "actions@github.com"')

    # Fetch headers and get filename
    file_created = fetch_headers()

    # Git commit and push
    run(f"git add {file_created}")
    run(f"git commit -m 'Headers snapshot {file_created}'")
    run("git push")
