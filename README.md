### Subdomain Enumeration Tool




This is a Python-based subdomain enumeration tool that performs DNS resolution and HTTP status code checks for given subdomains. It uses multithreading for faster execution and logs valid results to a file.

## Features
- **DNS Resolution**: Resolves subdomains using Google's DNS servers.
- **HTTP Status Code Filtering**: Logs subdomains with HTTP status codes **200**, **403**, or **302**.
- **Multithreading**: Speeds up enumeration by scanning multiple subdomains simultaneously.
- **Logging**: Saves results to `subdomain_scan_results.log` for later analysis.
- **Error Handling**: Skips subdomains with DNS or HTTP errors.

---

## Requirements
- **Python 3.x**
- Required Python modules:
  - `requests`
  - `dnspython`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/subdomain-enum-tool.git
   cd subdomain-enum-tool
   ```

2. Install the required Python modules:
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare a wordlist file (e.g., `subdomains.txt`) with potential subdomain names, one per line.

---

## Usage

Run the script using the following command:
```bash
python subdomain_enum.py <target_domain> <wordlist_file>
```

### Parameters:
- `<target_domain>`: The domain to scan for subdomains.
- `<wordlist_file>`: The path to the wordlist file containing subdomains to check.

### Example:
```bash
python subdomain_enum.py example.com subdomains.txt
```

---

## Output

### Console:
The tool displays found subdomains in green:
```plaintext
[+] Found: admin.example.com - HTTP Status: 200
[+] Found: login.example.com - HTTP Status: 403
[+] Found: redirect.example.com - HTTP Status: 302
```

### Log File:
Results are saved in `subdomain_scan_results.log`:
```plaintext
[+] Found: admin.example.com - HTTP Status: 200
[+] Found: login.example.com - HTTP Status: 403
[+] Found: redirect.example.com - HTTP Status: 302
```

---

## Customization

### Adding More Status Codes:
You can modify the `valid_status_codes` set in the script to include additional HTTP status codes:
```python
valid_status_codes = {200, 403, 302, 404}
```

---

## Notes
- **DNS Timeout**: The script uses Google's DNS servers and a timeout of 5 seconds per request.
- **HTTP Timeout**: HTTP requests have a timeout of 5 seconds.
- The tool skips subdomains that fail DNS resolution or return invalid HTTP status codes.

---
