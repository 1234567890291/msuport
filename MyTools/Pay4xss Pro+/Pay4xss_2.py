import requests
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time

# Initialize colorama for colorful CLI
init()

# Headers to bypass potential WAFs or restrictions
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "X-Forwarded-For": "127.0.0.1",
    "X-Originating-IP": "127.0.0.1",
    "Referer": "https://google.com/",
}

# Payload URLs
PAYLOAD_URLS = [
    "https://raw.githubusercontent.com/payloadbox/xss-payload-list/refs/heads/master/Intruder/xss-payload-list.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xor.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_advanced.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_more_advamced.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_payload.txt",
]

# Banner
def print_banner():
    print(Fore.YELLOW + Style.BRIGHT + """
██████╗  █████╗ ██╗   ██╗     ██╗  ██╗     ██╗  ██╗███████╗███████╗    
██╔══██╗██╔══██╗╚██╗ ██╔╝     ██║  ██║     ╚██╗██╔╝██╔════╝██╔════╝    
██████╔╝███████║ ╚████╔╝█████╗███████║█████╗╚███╔╝ ███████╗███████╗    
██╔═══╝ ██╔══██║  ╚██╔╝ ╚════╝╚════██║╚════╝██╔██╗ ╚════██║╚════██║    
██║     ██║  ██║   ██║             ██║     ██╔╝ ██╗███████║███████║    
╚═╝     ╚═╝  ╚═╝   ╚═╝             ╚═╝     ╚═╝  ╚══════╝╚══════╝    
                                                                        
""" + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Pay4xss Pro+ - Powerful XSS Detection Tool\n" + Style.RESET_ALL)

# Function to fetch payloads
def fetch_payloads():
    print(Fore.CYAN + "[+] Fetching payloads from the provided URLs..." + Style.RESET_ALL)
    payloads = []
    for url in PAYLOAD_URLS:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                payloads.extend(response.text.splitlines())
            else:
                print(Fore.RED + f"[-] Failed to fetch payloads from: {url} (Status Code: {response.status_code})" + Style.RESET_ALL)
        except requests.RequestException as e:
            print(Fore.RED + f"[-] Error fetching payloads from {url}: {e}" + Style.RESET_ALL)
    print(Fore.GREEN + f"[+] Payloads successfully loaded: {len(payloads)}\n" + Style.RESET_ALL)
    return payloads

# Function to inject payload intelligently into the URL
def inject_payload(url, payload):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if query_params:
        # Inject payload into existing parameters
        for param in query_params:
            query_params[param] = [payload]
    else:
        # Add new parameter if none exist
        query_params['q'] = [payload]
    
    new_query = urlencode(query_params, doseq=True)
    injected_url = urlunparse(
        parsed_url._replace(query=new_query)
    )
    return injected_url

# Function to test a URL for XSS vulnerabilities
def test_xss(url, payloads):
    print(Fore.CYAN + f"[+] Testing for XSS vulnerabilities on: {url}\n" + Style.RESET_ALL)
    for payload in payloads:
        start_time = time.time()
        try:
            # Inject payload into URL dynamically
            test_url = inject_payload(url, payload)
            response = requests.get(test_url, headers=HEADERS, timeout=10)
            elapsed_time = time.time() - start_time

            # Display status code, time taken, and analyze response for execution
            if response.status_code == 200:
                if "<script>" in response.text or "alert('XSS')" in response.text:
                    print(Fore.GREEN + f"[!!!] XSS Executed | Payload: {payload} | Status Code: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + f"[!] False Positive: Payload reflected but not executed. | Status Code: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"[-] Non-200 Response: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)

        except requests.RequestException as e:
            elapsed_time = time.time() - start_time
            print(Fore.RED + f"[-] Error testing payload: {payload} | {e} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)

# Main function
def main():
    print_banner()
    url = input(Fore.LIGHTYELLOW_EX + "Enter the target URL (e.g., https://www.example.com/): " + Style.RESET_ALL).strip()
    if not url:
        print(Fore.RED + "[-] Please provide a valid URL." + Style.RESET_ALL)
        return
    payloads = fetch_payloads()
    if payloads:
        test_xss(url, payloads)
    else:
        print(Fore.RED + "[-] No payloads to test. Exiting..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
