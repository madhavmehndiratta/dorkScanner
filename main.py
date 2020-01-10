import requests
import optparse
from functools import partial
from multiprocessing import Pool
from bs4 import BeautifulSoup as bsoup

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-s", '--search', dest="search", help="Specify the Search Query")
    parser.add_option("-e", '--engine', dest="engine", help="Specify the Search Engine (Google/Bing)")
    parser.add_option("-p", '--pages', dest="pages", help="Specify the Number of Pages (Default: 1)")
    parser.add_option("-P", '--processes', dest="processes", help="Specify the Number of Processes (Default: 1)")    
    (options, arguments) = parser.parse_args()
    return options


def google_search(query, page):
    base_url = "https://www.google.com/search"
    headers  = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0" }
    params   = { "q": query, "start": page * 10 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, "html.parser")
    links  = soup.findAll("cite")
    result = []
    for link in links:
        result.append(link.text)
    return result

def bing_search(query, page):
    base_url = "https://www.bing.com/search"
    headers  = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0" }
    params   = { "q": query, "first": page * 10 + 1 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, "html.parser")
    links  = soup.findAll("cite")
    result = []
    for link in links:
        result.append(link.text)
    return result

def search_result(q, engine, pages, processes, result):
    print("-" * 90)
    print(f"Searching for: {q} in {pages} page(s) of {engine} with {processes} processes")
    print("-" * 90)
    print()
    counter = 0
    for range in result:
        for r in range:
            print(r)
            counter += 1
    print()
    print("-" * 90)
    print(f"Number of urls: {counter}")
    print("-" * 90)

options = get_arguments()

def main():
    print("Welcome to the Dorks Scanner!")
    print()
    if not options.search:
        query = input("Enter the Search Query: ")
    else:
        query = options.search
    if not options.engine:
        engine = input("Choose the Search Engine (Google/Bing): ")
    else:
        engine = options.engine

    if engine.lower() == "google":
        target = partial(google_search, query)
    elif engine.lower() == "bing":
        target = partial(bing_search, query)

    else:
        print("Invalid Option Entered!...Exiting the Program....")
        exit()
    if not options.pages:
        pages = 1
    else:
        pages = options.pages

    if not options.processes:
        processes = 1
    else:
        processes = options.processes

    with Pool(processes) as p:
        result = p.map(target, range(pages))

    search_result(query, engine, pages, processes, result)

main()
startAgain = "y"
if not options.search and options.engine:
    startAgain = input("Do you want to try again? [y/n]: ")
    if startAgain.lower() == "y":
        main()
    else:
        exit()
else:
    exit()