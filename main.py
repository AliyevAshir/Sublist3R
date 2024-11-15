import requests
import dns.resolver
from queue import Queue
import threading
import sys

# Function to log found subdomains
def log_found_subdomain(message):
    with open("subdomain_scan_results.log", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

# Function to check subdomain via DNS and HTTP
def check_subdomain(target_domain, subdomain, queue):
    full_domain = f"{subdomain}.{target_domain}"
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 10
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google DNS

    # List of HTTP status codes to log
    valid_status_codes = {200, 403, 302}

    try:
        # Perform DNS resolution
        dns.resolver.resolve(full_domain, "A")

        # If DNS resolution succeeds, try HTTP request
        try:
            response = requests.get(f"http://{full_domain}", timeout=5)
            if response.status_code in valid_status_codes:
                message = f"[+] Found: {full_domain} - HTTP Status: {response.status_code}"
                print(f"\033[92m{message}\033[0m")  # Green for valid codes
                log_found_subdomain(message)
        except requests.exceptions.RequestException:
            pass  # Ignore HTTP errors if DNS resolves

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        pass  # Ignore non-existent domains or timeouts

    except Exception as e:
        print(f"[!] Error: {full_domain} - {str(e)}")

    finally:
        queue.task_done()

# Multithreaded subdomain enumeration function
def subdomain_enum(target_domain, wordlist):
    queue = Queue()

    # Load subdomains from the wordlist
    try:
        with open(wordlist, "r") as file:
            subdomains = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {wordlist}")
        sys.exit(1)

    print(f"[*] Starting enumeration for {target_domain} with {len(subdomains)} subdomains.\n")
    print("[*] Results will be saved in 'subdomain_scan_results.log'.")

    # Create threads for subdomain enumeration
    for subdomain in subdomains:
        queue.put(subdomain)
        thread = threading.Thread(target=check_subdomain, args=(target_domain, subdomain, queue))
        thread.daemon = True
        thread.start()

    queue.join()  # Wait for all tasks to be completed
    print("\n[*] Enumeration completed. Check 'subdomain_scan_results.log' for results.")

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python subdomain_enum.py <target_domain> <wordlist_file>")
        sys.exit(1)

    target_domain = sys.argv[1]
    wordlist = sys.argv[2]

    # Start subdomain enumeration
    subdomain_enum(target_domain, wordlist)

if __name__ == "__main__":
    main()
