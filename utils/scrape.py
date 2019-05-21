from googlesearch import search
import requests
import urllib
from bs4 import BeautifulSoup

def google_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.title.text

if __name__ == '__main__':
    query = 'Response object above tell'
    for url in search(query, stop=3):
        a = google_scrape(url)
        print("url", url)
        print ("Title: " + a)
        print (" ")

