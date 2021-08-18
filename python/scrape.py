import re
import requests
import os
from bs4 import BeautifulSoup

def get_author(name):
    urls = []
    temp = name.split()
    url = "https://www.gutenberg.org/ebooks/authors/search/?query=" + "+".join(temp).lower()
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for a in soup.find_all('a', href=True):
        if len(re.findall('\\b' + 'author' + '\\b', a['href'])) > 0:
            url = "https://www.gutenberg.org" + a['href']
            urls.append("https://www.gutenberg.org" + a['href'])
            break
        else:
            print("Author not Available")
            quit()
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    while len(soup.select('a[accesskey="+"]')) > 0:
        url = "https://www.gutenberg.org" + soup.select('a[accesskey="+"]')[0]['href']
        urls.append("https://www.gutenberg.org" + soup.select('a[accesskey="+"]')[0]['href'])
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return (urls, temp)


def get_books(urls, language):
    links = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        for a in soup.find_all('a', href=True):
            if len(re.findall('/ebooks/' + '\\d+', a['href'])) > 0:
                for c in a.contents:
                    if "title" in str(c):
                        if "Project Gutenberg Works of" in str(c):
                            continue
                        else:
                            if language.title() == "English" and "(" not in str(c):
                                links.append("https://www.gutenberg.org" + a['href'])
                            elif language.title() in str(c):
                                links.append("https://www.gutenberg.org" + a['href'])
    if len(links) == 0:
        print("Author not available in this language")
    return links


def download_books(links, name, format):
    os.chdir(os.path.join(os.path.abspath(os.getcwd()), 'data'))
    os.makedirs(os.path.join(os.getcwd(), "_".join(name).title()))
    downloads = os.path.abspath("_".join(name).title())
    for link in links:
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        for a in soup.find_all('a', href=True):
            if format in a['href']:
                if 'readme' in a['href']:
                    continue
                else:
                    book = open(os.path.join(downloads,os.path.basename(a['href'])),'wb')
                    for chunk in requests.get('https:' + a['href']).iter_content(100000):
                        book.write(chunk)
                    book.close()


def download(name, language="English", format=".txt"):
    r, t = get_author(name)
    l = get_books(r, language)
    download_books(l, t, format)
