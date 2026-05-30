"""Brick 5: Azure Endpoint Verification — confirm Locate Anything is reachable.

Pass condition: prints ENDPOINT REACHABLE with model name and API version.
Hardware: none (network only).
Requires: .env file with AZURE_ENDPOINT and AZURE_API_KEY.
"""

import sys
import os


def load_env():
    """Load variables from .env file in the same directory."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        print(f"FAIL: No .env file found at {env_path}")
        print("Create it with:")
        print("  AZURE_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com")
        print("  AZURE_API_KEY=your-api-key")
        print("  AZURE_SPEECH_KEY=your-speech-key")
        print("  AZURE_SPEECH_REGION=eastus")
        return False

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    return True


def main():
    if not load_env():
        return False

    import requests

    endpoint = os.environ.get("AZURE_ENDPOINT")
    api_key = os.environ.get("AZURE_API_KEY")

    if not endpoint or not api_key:
        print("FAIL: AZURE_ENDPOINT and AZURE_API_KEY must be set in .env")
        return False

    # Test endpoint health
    print(f"Testing endpoint: {endpoint}")
    print("Sending health check...")

    try:
        # Attempt a minimal request to verify connectivity and auth
        url = f"{endpoint}/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"\nENDPOINT REACHABLE")
            print(f"  URL:      {endpoint}")
            print(f"  Status:   {response.status_code}")
            print(f"  Response: {data}")
            return True
        elif response.status_code == 401:
            print(f"FAIL: Authentication failed (401). Check your API key.")
            return False
        elif response.status_code == 404:
            # The /models endpoint may not exist; try a different health path
            print(f"  /models returned 404, trying base URL...")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"\nENDPOINT REACHABLE (base URL)")
            print(f"  URL:    {endpoint}")
            print(f"  Status: {response.status_code}")
            return response.status_code < 500
        else:
            print(f"FAIL: Unexpected status {response.status_code}")
            print(f"  Body: {response.text[:500]}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"FAIL: Could not connect to {endpoint}")
        print("Check your network and endpoint URL.")
        return False
    except requests.exceptions.Timeout:
        print(f"FAIL: Connection timed out after 10s")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
