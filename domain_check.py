'''
Domain Availability Checker Tool

This script checks if domains listed in a text file are available for registration.

Dependencies:
    pip install python-whois

Usage:
    python domain_check.py --input domains.txt --output results

Outputs:
    results_available.txt   # domains likely available
    results_unavailable.txt # domains likely registered or resolving
'''

import argparse
import whois
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_domain(domain: str) -> (str, bool):
    """
    Check if a single domain is available.
    Returns a tuple of (domain, is_available).
    """
    domain = domain.strip()
    if not domain:
        return domain, False

    is_taken = False
    try:
        w = whois.whois(domain)
        if w.domain_name:
            is_taken = True
    except Exception:
        # WHOIS lookup failed or returned no data
        pass

    if not is_taken:
        try:
            socket.gethostbyname(domain)
            is_taken = True
        except socket.gaierror:
            is_taken = False

    # If taken => unavailable, else available
    return domain, not is_taken


def main(input_file: str, output_prefix: str, workers: int = 20):
    # Read domains from input file
    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]

    available = []
    unavailable = []

    # Use ThreadPoolExecutor for faster lookups
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_domain = {executor.submit(check_domain, d): d for d in domains}
        for future in as_completed(future_to_domain):
            domain, is_available = future.result()
            if is_available:
                available.append(domain)
            else:
                unavailable.append(domain)

    # Write output files
    avail_file = f"{output_prefix}_available.txt"
    unavail_file = f"{output_prefix}_unavailable.txt"

    with open(avail_file, 'w') as fa:
        for d in available:
            fa.write(d + '\n')

    with open(unavail_file, 'w') as fu:
        for d in unavailable:
            fu.write(d + '\n')

    print(f"Checked {len(domains)} domains.")
    print(f"Available: {len(available)} (see {avail_file})")
    print(f"Unavailable: {len(unavailable)} (see {unavail_file})")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Domain Availability Checker')
    parser.add_argument('--input', '-i', required=True,
                        help='Path to text file with domains (one per line)')
    parser.add_argument('--output', '-o', required=True,
                        help='Prefix for output files')
    parser.add_argument('--workers', '-w', type=int, default=20,
                        help='Number of concurrent threads (default: 20)')
    args = parser.parse_args()

    main(args.input, args.output, args.workers)
