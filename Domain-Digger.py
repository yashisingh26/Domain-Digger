#!/usr/bin/env python3

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

banner = rf"""{GREEN}



██████   ██████  ███    ███  █████  ██ ███    ██     ██████  ██  ██████   ██████  ███████ ██████  
██   ██ ██    ██ ████  ████ ██   ██ ██ ████   ██     ██   ██ ██ ██       ██       ██      ██   ██ 
██   ██ ██    ██ ██ ████ ██ ███████ ██ ██ ██  ██     ██   ██ ██ ██   ███ ██   ███ █████   ██████  
██   ██ ██    ██ ██  ██  ██ ██   ██ ██ ██  ██ ██     ██   ██ ██ ██    ██ ██    ██ ██      ██   ██ 
██████   ██████  ██      ██ ██   ██ ██ ██   ████     ██████  ██  ██████   ██████  ███████ ██   ██ 
                                                                                                  
                                                                                                  
                                         
{RED}Developer : Yashi Singh{RESET}
"""

print(banner)

import requests
import argparse
import sys
from gevent import socket
from gevent.pool import Pool

requests.packages.urllib3.disable_warnings()

def main(domain, masscanOutput, urlOutput):
    domainsFound = {}
    domainsNotFound = {}

    if not masscanOutput and not urlOutput:
        print("[+]: Downloading domain list from crt.sh...")

    response = collectResponse(domain)

    if not masscanOutput and not urlOutput:
        print("[+]: Download of domain list complete.")

    domains = collectDomains(response)

    if not masscanOutput and not urlOutput:
        print(f"[+]: Parsed {len(domains)} domain(s) from list.")

    if len(domains) == 0:
        print("[!]: No domains found.")
        exit(1)

    pool = Pool(15)
    greenlets = [pool.spawn(resolve, domain) for domain in domains]
    pool.join(timeout=1)

    for greenlet in greenlets:
        result = greenlet.value
        if result:
            for ip in result.values():
                if ip != 'none':
                    domainsFound.update(result)
                else:
                    domainsNotFound.update(result)

    if urlOutput:
        printUrls(sorted(domainsFound))
    if masscanOutput:
        printMasscan(domainsFound)
    if not masscanOutput and not urlOutput:
        print("\n[+]: Domains found:")
        printDomains(domainsFound)
        print("\n[+]: Domains with no DNS record:")
        printDomains(domainsNotFound)


def resolve(domain):
    try:
        return {domain: socket.gethostbyname(domain)}
    except:
        return {domain: "none"}


def printDomains(domains):
    for domain in sorted(domains):
        print(f"{domains[domain]}\t{domain}")


def printMasscan(domains):
    iplist = set()
    for domain in domains:
        iplist.add(domains[domain])
    for ip in sorted(iplist):
        print(ip)


def printUrls(domains):
    for domain in domains:
        print(f"https://{domain}")


def collectResponse(domain):
    url = f'https://crt.sh/?q={domain}&output=json'
    try:
        response = requests.get(url, verify=False)
    except:
        print("[!]: Connection to server failed.")
        exit(1)
    try:
        return response.json()
    except:
        print("[!]: The server did not respond with valid JSON.")
        exit(1)


def collectDomains(response):
    domains = set()
    for domain in response:
        domains.add(domain['common_name'])
        if '\n' in domain['name_value']:
            domlist = domain['name_value'].split()
            for dom in domlist:
                domains.add(dom)
        else:
            domains.add(domain['name_value'])
    return domains


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str,
                        help="domain to query for CT logs, e.g.: domain.com")
    parser.add_argument("-u", "--urls", default=0, action="store_true",
                        help="output results with https:// URLs for domains that resolve, one per line.")
    parser.add_argument("-m", "--masscan", default=0, action="store_true",
                        help="output resolved IP address, one per line. Useful for masscan IP list import \"-iL\" format.")

    # If no arguments passed, show help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    if not args.domain:
        print("[!] Please provide a domain using -d or --domain.")
        sys.exit(1)

    main(args.domain, args.masscan, args.urls)
