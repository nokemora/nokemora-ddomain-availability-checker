# Domain Availability Checker

A Python script to check the availability of domain names in bulk using WHOIS and DNS lookup.

---

## Features

- Reads a list of domains from a plain text file (one domain per line).
- Checks each domain's availability using WHOIS and DNS resolution.
- Supports multithreading for faster processing.
- Outputs two files:
  - `results_available.txt` — domains likely available for registration.
  - `results_unavailable.txt` — domains already registered or resolving.

---

## Requirements

- Python 3.7+
- `python-whois` library

Install the required package:

```bash
pip install python-whois
Usage
Prepare a text file with your list of domains (e.g., domains.txt), one per line.

Run the script:

bash
Copy
Edit
python domain_check.py --input domains.txt --output results
After running, check the output files:

results_available.txt

results_unavailable.txt

Example domains.txt
Copy
Edit
HoustonFitnessCoach.com
ExampleSite.com
MyTestDomain.org
Notes
The script uses WHOIS lookup first and then falls back to DNS resolution to determine availability.

For large lists, adjust concurrency with the --workers option (default is 20):

bash
Copy
Edit
python domain_check.py --input domains.txt --output results --workers 10
License
This project is licensed under the MIT License.

Author
Your Name or GitHub Username
