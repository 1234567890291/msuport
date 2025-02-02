import requests
from colorama import Fore, Style, init
from urllib.parse import urlparse
import time
from tqdm import tqdm  # Progress bar
import threading
import sys
import os

os.system("cls")
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
# Payload URLs
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


# Banner
def print_banner():
    print(Fore.GREEN + Style.BRIGHT + """
██████╗  █████╗ ██╗   ██╗     ██╗  ██╗     ██╗  ██╗███████╗███████╗
██╔══██╗██╔══██╗╚██╗ ██╔╝     ██║  ██║     ╚██╗██╔╝██╔════╝██╔════╝
██████╔╝███████║ ╚████╔╝█████╗███████║█████╗╚███╔╝ ███████╗███████╗
██╔═══╝ ██╔══██║  ╚██╔╝ ╚════╝╚════██║╚════╝██╔██╗ ╚════██║╚════██║
██║     ██║  ██║   ██║             ██║     ██╔╝ ██╗███████║███████║
╚═╝     ╚═╝  ╚═╝   ╚═╝             ╚═╝     ╚══╝ ╚══════╝╚══════╝

        There are total 27039 XSS payload in this tool
          Visit pay4xss.vercel.app for moreinfo
""" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Pay4xss Pro+ - Powerful XSS Detection Tool" + Style.RESET_ALL)

# Function to fetch API keys from the code.txt
def fetch_api_keys():
    try:
        response = requests.get("https://pay4xss-git-main-1234567890291s-projects.vercel.app/img/code.txt")
        if response.status_code == 200:
            return response.text.strip().split('\n')
        else:
            print(Fore.RED + "[-] Failed to fetch the API keys list from the URL." + Style.RESET_ALL)
            return []
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error fetching API keys: {e}" + Style.RESET_ALL)
        return []

# Function to validate API key
def validate_api_key(api_key):
    keys = fetch_api_keys()
    if any(api_key in key for key in keys):  # Check if the API key exists in the list
        return True
    return False

# Function to fetch payloads with animation
def fetch_payloads():
    print(Fore.CYAN + "[+] Checking... (This is Depend on your network speed)" + Style.RESET_ALL)
    payloads = []
    
    # Display a loading animation while fetching payloads
    def loading_animation():
        animation = "|/-\\"
        i = 0
        while not done_fetching[0]:
            sys.stdout.write(f"\r{Fore.YELLOW}[+] Fetching payloads... {animation[i % len(animation)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r")  # Clear line

    done_fetching = [False]  # To control animation thread

    # Start the loading animation in a separate thread
    threading.Thread(target=loading_animation, daemon=True).start()

    for url in PAYLOAD_URLS:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                payloads.extend(response.text.splitlines())
            else:
                print(Fore.RED + f"[-] Failed to fetch payloads from: {url} (Status Code: {response.status_code})" + Style.RESET_ALL)
        except requests.RequestException as e:
            print(Fore.RED + f"[-] Error fetching payloads from {url}: {e}" + Style.RESET_ALL)
    
    done_fetching[0] = True  # Stop animation
    print(Fore.GREEN + f"[+] Payloads successfully loaded: {len(payloads)}\n" + Style.RESET_ALL)
    return payloads

# Function to inject payload intelligently into the URL
def inject_payload(url, payload):
    return url + payload

# Function to test a URL for XSS vulnerabilities with animation
def test_xss(url, payloads):
    print(Fore.CYAN + f"[+] Testing for XSS vulnerabilities on: {url}\n" + Style.RESET_ALL)
    
    for payload in tqdm(payloads, desc="Testing payloads", unit="payload"):
        start_time = time.time()
        try:
            # Inject payload into URL dynamically
            test_url = inject_payload(url, payload)
            response = requests.get(test_url, headers=HEADERS, timeout=10)
            elapsed_time = time.time() - start_time

            # Display status code, time taken, and analyze response for execution
            if response.status_code == 200:
                if "<script>" in response.text or "alert('XSS')" in response.text:
                    print(Fore.GREEN + f"[!!!] XSS Executed | Payload: {payload} | Status Code: {response.status_code} | Time: {elapsed_time:.2f}s" + Style.RESET_ALL)
        except requests.RequestException as e:
            print(Fore.RED + f"[-] Error with payload {payload} on URL {url}: {e}" + Style.RESET_ALL)

# Main execution
def main():
    print_banner()

    api_key = input(Fore.YELLOW + "Please enter your API key to proceed: " + Style.RESET_ALL)

    if not validate_api_key(api_key):
        print(Fore.RED + "[-] Invalid API key. Access Denied." + Style.RESET_ALL)
        return

    url = input(Fore.YELLOW + "Enter the URL to test for XSS (e.g., https://example.com): " + Style.RESET_ALL)

    # Validate URL
    if not urlparse(url).scheme:
        print(Fore.RED + "[-] Invalid URL format. Please include 'http://' or 'https://'." + Style.RESET_ALL)
        return

    # Fetch payloads
    payloads = fetch_payloads()

    # Test XSS
    test_xss(url, payloads)

if __name__ == "__main__":
    main()
