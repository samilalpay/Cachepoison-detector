import requests
from utils.diff import show_body_diff

def send_request(url, headers=None):
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return {
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.text
        }
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return None

def compare_responses(normal, poisoned):
    differences = []

    if normal['status_code'] != poisoned['status_code']:
        differences.append(f"Status Code: {normal['status_code']} ➡️ {poisoned['status_code']}")

    for key in set(normal['headers'].keys()).union(poisoned['headers'].keys()):
        val1 = normal['headers'].get(key)
        val2 = poisoned['headers'].get(key)
        if val1 != val2:
            differences.append(f"Header '{key}': {val1} ➡️ {val2}")

    if normal['body'] != poisoned['body']:
        differences.append("Body differs:")
        body_diffs = show_body_diff(normal['body'], poisoned['body'])
        differences.extend(body_diffs)

    return differences
