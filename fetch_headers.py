import requests
import subprocess
from datetime import datetime, timezone

WEBSITES = {
    "airtel": "https://www.airtel.in",
    "jio": "https://www.jio.com",
    "phonepe": "https://www.phonepe.com",
    "flipkart": "https://www.flipkart.com",
    "paytm": "https://paytm.com"
}

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def fetch_headers():
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

if __name__ == "__main__":
    file_created = fetch_headers()
    run(f"git add {file_created}")
    run(f"git commit -m 'Headers snapshot {file_created}'")
    run("git push")
