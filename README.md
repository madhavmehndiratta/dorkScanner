# DORK SCANNER #

A typical search engine dork scanner scrapes search engines with dorks that you provide in order to find vulnerable URLs.


## Introduction ##

Dorking is a technique used by newsrooms, investigative organisations, security auditors as well as tech savvy criminals to query various search engines for information hidden on public websites and vulnerabilities exposed by public servers. Dorking is a way of using search engines to their full capacity to penetrate web-based services to depths that are not necessarily visible at first.

## Requirements ##

```
pip install -r requirements.txt
```

## Usage ##

```
$ python3 main.py --help
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -s SEARCH, --search=SEARCH
                        Specify the Search Query
  -e ENGINE, --engine=ENGINE
                        Specify the Search Engine (Google/Bing)
  -p PAGES, --pages=PAGES
                        Specify the Number of Pages (Default: 1)
  -P PROCESSES, --processes=PROCESSES
                        Specify the Number of Processes (Default: 1)
```

You can also specify the arguments inside the program:

```
Welcome to the Dorks Scanner!

Enter the Search Query: 
Choose the Search Engine (Google/Bing):
```

## Tutorial ##

[![asciicast](https://asciinema.org/a/7INNpb1cxNcXXNGjUDlTfzLbY.png)](https://asciinema.org/a/7INNpb1cxNcXXNGjUDlTfzLbY)
