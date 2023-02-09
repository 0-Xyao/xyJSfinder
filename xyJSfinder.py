import argparse
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import time
import datetime

def print_logo():
    print("""
                _ ____   __ _           _           
__  ___   _    | / ___| / _(_)_ __   __| | ___ _ __ 
\ \/ / | | |_  | \___ \| |_| | '_ \ / _` |/ _ \ '__|
 >  <| |_| | |_| |___) |  _| | | | | (_| |  __/ |   
/_/\_\\__, |\___/|____/|_| |_|_| |_|\__,_|\___|_|   
      |___/                                         
By：小妖
UpdateTime：2023/02/09
GitHub：https://github.com/0-Xyao/xyJSfinder
欢迎使用xyJSfinder - 一个爬取web页面js内的url并批量进行存活探测                                
                                                """)

def print_usage():
    print("""
Usage: python3 xyJSfinder.py [OPTIONS]

Examples:
  python3 xyJSfinder.py  -u https://www.example.com

    """)

print_logo()
def extract_links_from_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        scripts = [script.get('src') for script in soup.find_all('script')]
        print('[---]爬取JS URL LINKS ')
        print('[+] URL Links:')
        for link in links:
            print(link)
        print('\n[++++++] JS Files found:')
        for script in scripts:
            print(script)
    else:
        print(f'Failed to retrieve page: {response.status_code}')
        
    return links

def scan_site(url):
    links = extract_links_from_page(url)
    
    print('\n[+] Web Dirscan:')
    print(f'URL加载地址{url}')
    for link in links:
        if link.startswith('/'):
            link = url + link
        try:
            response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'})
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title').text
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(colored(f'「{current_time}」：{colored(link, "blue")} - [status: {colored(response.status_code, "green")} Size:{colored(len(response.content), "green")} Title:{colored(title, "green")}]'))
            print()
        except Exception as e:
            print(f'Failed to retrieve {link}: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scan a website for links and scripts')
    parser.add_argument('-u', '--url', required=True, help='The URL of the website to scan')
    args = parser.parse_args()
    scan_site(args.url)