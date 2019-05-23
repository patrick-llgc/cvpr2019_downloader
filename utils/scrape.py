from googlesearch import search
import requests
from requests import get  # to make GET request
from bs4 import BeautifulSoup
import googlesearch
import json
import random
import time
import os

def google_scrape(url):
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.title.text


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


def get_arxiv_urls(paper_titles, output_json_dir=None):
    """Get a list of arxiv urls from paper_titles

    One way to do it is to install googler and use it.
    ```
    for filename in files[:1]:
        os.system('googler -n 1 "{}" arxiv.org filetype:pdf'.format(filename))
    ```

    Note that google search has a query limit. Per instructions here:
    https://github.com/abenassi/Google-Search-API/blob/master/google/modules/utils.py#L81
    >>  You may also wanna wait some time between queries, say, randint(50,65)
        between each query, and randint(180,240) every 100 queries, which is
        what I found useful.

    Here we use python lib googlesearch for portability

    TODO: try https://github.com/abenassi/Google-Search-API to avoid double query
    """
    urls = []
    for idx_query, paper_title in tqdm(list(enumerate(paper_titles[:]))):
        success = False
        num_trial = 0
        sleep_in_seconds = 0
        query_results = []
        query = '{} arxiv.org'.format(paper_title)
        print(query)
        # try num_trial times with sleep_in_seconds intervals before moving on to next search
        while not success and num_trial < 2:
            time.sleep(sleep_in_seconds)
            try:
                # convert returned iterator to list to catch the error here
                query_results = list(googlesearch.search(query, stop=1, pause=2))
            except:
                sleep_in_seconds = random.randint(180, 240) * (num_trial + 1)
                print('Warning: sleep and retry in {} seconds'.format(sleep_in_seconds))
                continue
            num_trial += 1
            success = True

        for url in query_results:
            if 'arxiv.org/pdf' in url:
                # cannot scrape the title of a web page containing a pdf file
                continue
            # sometimes google gives a numeric IP as of arxiv.
            url = 'https://arxiv.org/' + '/'.join(url.replace('https://', '').split('/')[-2:])
            try:
                url_title = google_scrape(url)
            except:
                url_title = ''
            print('url ', url)
            print('url title ', url_title)
            urls.append({
                'url_title': url_title,
                'url': url,
                'query': paper_title,
            })
    if os.path.isdir(output_json_dir):
        with open(os.path.join(output_json_dir, 'query_urls.json'), 'a') as f_out:
            json.dump(urls, f_out, indent=4, sort_keys=True)
    return urls


if __name__ == '__main__':
    query = 'Response object above tell'
    for url in search(query, stop=3):
        a = google_scrape(url)
        print("url", url)
        print ("Title: " + a)
        print (" ")

