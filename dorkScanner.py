import requests
import argparse
from functools import partial
from multiprocessing import Pool
from bs4 import BeautifulSoup as bsoup


GREEN, RED = '\033[1;32m', '\033[91m'


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', dest='query', help='Specify the Search Query within \'\'')
    parser.add_argument('-e', '--engine', dest='engine', help='Specify the Search Engine (Google/Bing)')
    parser.add_argument('-p', '--pages', dest='pages', help='Specify the Number of Pages (Default: 1)')
    parser.add_argument('-P', '--processes', dest='processes', help='Specify the Number of Processes (Default: 2)')    
    options = parser.parse_args()
    return options


def google_search(query, page):
    base_url = 'https://www.google.com/search'
    headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
    params   = { 'q': query, 'start': page * 10 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, 'html.parser')
    links = soup.findAll("div", { "class" : "yuRUbf" })
    result = []
    for link in links:
        result.append(link.find('a').get('href'))
    return result


def bing_search(query, page):
    base_url = 'https://www.bing.com/search'
    headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
    params   = { 'q': query, 'first': page * 10 + 1 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, 'html.parser')
    links  = soup.findAll('cite')
    result = []
    for link in links:
        result.append(link.text)
    return result


def search_result(q, engine, pages, processes, result):
    print('-' * 70)
    print(f'Searching for: {q} in {pages} page(s) of {engine} with {processes} processes')
    print('-' * 70)
    print()
    counter = 0
    for range in result:
        for r in range:
            print('[+] ' + r)
            counter += 1
    print()
    print('-' * 70)
    print(f'Number of urls: {counter}')
    print('-' * 70)


options = get_arguments()

banner = ''' 

    ██████╗░░█████╗░██████╗░██╗░░██╗  ░██████╗░█████╗░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
    ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝  ██╔════╝██╔══██╗██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
    ██║░░██║██║░░██║██████╔╝█████═╝░  ╚█████╗░██║░░╚═╝███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
    ██║░░██║██║░░██║██╔══██╗██╔═██╗░  ░╚═══██╗██║░░██╗██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
    ██████╔╝╚█████╔╝██║░░██║██║░╚██╗  ██████╔╝╚█████╔╝██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
    ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
    
    Made By: Madhav Mehndiratta (github.com/madhavmehndiratta) 

'''


def main():
    print()
    if not options.query:
        query = input('[?] Enter the Search Query: ')
    else:
        query = options.query
    if not options.engine:
        engine = input('[?] Choose the Search Engine (Google/Bing): ')
    else:
        engine = options.engine

    if engine.lower() == 'google':
        target = partial(google_search, query)
    elif engine.lower() == 'bing':
        target = partial(bing_search, query)

    else:
        print('[-] Invalid Option Entered!...Exiting the Program....')
        exit()
    if not options.pages:
        pages = 1
    else:
        pages = options.pages

    if not options.processes:
        processes = 2
    else:
        processes = options.processes

    with Pool(int(processes)) as p:
        result = p.map(target, range(int(pages)))

    search_result(query, engine, pages, processes, result)


print(GREEN + banner)

try:
    main()
    while True:
        if options.query and options.engine:
            exit()
        else:
            main()
except KeyboardInterrupt:
    print('\nThanks For using!')
    exit()
except TimeoutError:
    print(RED + '\n[-] Too many requests, please try again later....')
    exit()
