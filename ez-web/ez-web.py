#!/usr/bin/env python3
import string
import requests
import base64
import re
import argparse
from urllib.parse import urlparse


URLS = []
BASE_URL = ''

blue = '\033[94m'
cyan = '\033[96m'
info = '\033[93m'
green = '\033[92m'
red = '\033[91m'
end = '\033[0m'


def handle_git(response):
    if response.status_code == 200:
        print(f"{green}git found{end}")
        print(f"{cyan}{response.text}{end}")


def handle_security(response):
    if response.status_code == 200:
        print(f"{green}security.txt found{end}")
        print(f"{cyan}{response.text}{end}")


def handle_robots(response):
    if response.status_code == 200:
        print(f"{green}robots.txt found{end}")
        print(f"{cyan}{response.text}{end}")
        regex = re.compile(r'Disallow: (.*)')
        paths = regex.findall(response.text)
        for path in paths:
            add_url(BASE_URL + path)


INTERESTING_PATHS = {
    "robots.txt": handle_robots,
    ".well-known/security.txt": handle_security,
    ".git/HEAD": handle_git,
    ".DS_Store": lambda r: print(f"{green}.DS_Store found{end}"),
    ".gitignore": lambda r: print(f"{green}.gitignore found{end}"),
    ".git/config": lambda r: print(f"{green}.git/config found{end}"),
}


def add_url(url):
    if url not in URLS:
        URLS.append(url)


def find_urls(regex, url, response):
    urls = regex.findall(response)
    for url in urls:
        if url.startswith('http'):
            add_url(url)
        elif url.startswith('//'):
            add_url('https:' + url)
        elif url.startswith('/'):
            add_url(BASE_URL + url)
        else:
            add_url(BASE_URL + '/' + url)


def check_urls(url, response):
    find_urls(re.compile(r'href=\"([^\"]+)'), url, response)
    find_urls(re.compile(r'<script.*src="(.*)"'), url, response)


def check_comments(response):
    html_comments = re.compile(r'\<\!\-\-(?:.|\n|\r)*?-->')
    comments = html_comments.findall(response)
    for comment in comments:
        print(f"{cyan}HTML comment found: {comment}{end}")
    block_comments = re.compile(r'/\*.*?\*/|/\*[\s\S]*?\*/')
    comments = block_comments.findall(response)
    for comment in comments:
        print(f"{cyan}Block comment found: {comment}{end}")
    line_comments = re.compile(r'// (.*)')
    comments = line_comments.findall(response)
    for comment in comments:
        print(f"{cyan}Line comment found: {comment}{end}")


def check_response(response):
    check_comments(response)
    flag_regex = re.compile(r'[A-Za-z0-9]{1,}{[A-Za-z0-9\_\-\?\!]{3,}}')
    flag = flag_regex.findall(response)
    if flag:
        print(f"{green}Flag found: {flag[0]}{end}")
    base64_regex = re.compile(r'[A-Za-z0-9+\/]{6,}[=]{0,2}')
    base64_data = base64_regex.findall(response)
    for data in base64_data:
        try:
            decoded = base64.b64decode(data).decode('utf-8')
            if all(c in string.printable for c in decoded):
                print(f"{cyan}Base64 data found: {data}{end}")
                print(f"{cyan}Decoded: {decoded}{end}")
        except:
            pass


def print_banner():
    print(f"""{blue}
@@@@@@@@  @@@@@@@@             @@@  @@@  @@@  @@@@@@@@  @@@@@@@
@@@@@@@@  @@@@@@@@             @@@  @@@  @@@  @@@@@@@@  @@@@@@@@
@@!            @@!             @@!  @@!  @@!  @@!       @@!  @@@
!@!           !@!              !@!  !@!  !@!  !@!       !@   @!@
@!!!:!       @!!    @!@!@!@!@  @!!  !!@  @!@  @!!!:!    @!@!@!@
!!!!!:      !!!     !!!@!@!!!  !@!  !!!  !@!  !!!!!:    !!!@!!!!
!!:        !!:                 !!:  !!:  !!:  !!:       !!:  !!!
:!:       :!:                  :!:  :!:  :!:  :!:       :!:  !:!
 :: ::::   :: ::::              :::: :: :::    :: ::::   :: ::::
: :: ::   : :: : :               :: :  : :    : :: ::   :: : ::
          {end}""")


if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL to request', required=True)
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    if not parsed_url.scheme:
        parsed_url = urlparse('https://' + args.url)
    BASE_URL = parsed_url.scheme + '://' + parsed_url.netloc

    URLS.append(parsed_url.geturl())

    s = requests.Session()
    for path, handler in INTERESTING_PATHS.items():
        r = s.get(BASE_URL + '/' + path)
        handler(r)

    for url in URLS:
        if not url.startswith(BASE_URL):
            continue

        print(f"{info}Checking {url}{end} ", end='...')
        r = s.get(url)
        if r.status_code == 200:
            print(f"{green}Found{end}")
        else:
            print(f"{red}Not found{end}")

        check_response(r.text)
        check_urls(url, r.text)
