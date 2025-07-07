from utils.requester import send_request, compare_responses
from utils.payloads import payload_headers, generate_payload_mutations
from utils.diff import show_body_diff

def scan_with_mutations(url, normal_response, base_payload):
    mutations = generate_payload_mutations(base_payload)
    print(f"[*] Total {len(mutations)} mutations generated for payload: {base_payload}")

    for mutated in mutations:
        for header in payload_headers.keys():
            print(f"\n[>] Testing header: {header} with payload: {mutated}")
            headers = {
                header: mutated
            }
            poisoned = send_request(url, headers=headers)
            if not poisoned:
                continue

            diffs = compare_responses(normal_response, poisoned)
            if diffs:
                print(f"    [!] Difference found with mutation '{mutated}' in header '{header}':")
                for diff in diffs:
                    print("       -", diff)

def main():
    url = input("Enter target URL (e.g., http://127.0.0.1:8080/test): ").strip()
    print("\n[*] Sending normal request...")
    normal_response = send_request(url)

    if not normal_response:
        print("[!] Could not get normal response.")
        return

    print("\n[*] Testing headers with base payloads...")
    for header, payload in payload_headers.items():
        print(f"\n[>] Testing header: {header}")
        headers = {header: payload}
        poisoned = send_request(url, headers=headers)
        if not poisoned:
            continue

        diffs = compare_responses(normal_response, poisoned)
        if diffs:
            print(f"    [!] Difference found for header '{header}':")
            for diff in diffs:
                print("       -", diff)

    print("\n[*] Starting WAF Bypass Mutation Scans...")
    scan_with_mutations(url, normal_response, base_payload="evil.com")

if __name__ == "__main__":
    main()
