import os
import googlesearch
import json
from tqdm import tqdm
from utils.scrape import google_scrape
from utils.extract_pdf import batch_extract_from_folder


class FileDownloadAndCombinerConfig(object):
    paper_list_txt = './assets/orals.txt'
    dl_dir = './papers'


class FileDownloadAndCombiner(object):
    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_paper_titles(paper_list_txt):
        with open(paper_list_txt, 'r') as f_in:
            paper_titles = f_in.readlines()
        paper_titles = [x.strip() for x in paper_titles[1:]]
        print('{} papers loaded'.format(len(paper_titles)))
        return paper_titles

    @staticmethod
    def get_arxiv_urls(paper_titles):
        """Get a list of arxiv urls from paper_titles

        One way to do it is to install googler and use it.
        ```
        for filename in files[:1]:
            os.system('googler -n 1 "{}" arxiv.org filetype:pdf'.format(filename))
        ```

        Here we use python lib ??? for portability
        """
        urls = []
        for paper_title in tqdm(paper_titles[:]):
            query = '{} arxiv.org'.format(paper_title)
            print(query)
            for url in googlesearch.search(query, stop=1):
                print(url)
                if 'arxiv.org/pdf' in url:
                    # cannot scrape the title of a web page containing a pdf file
                    continue
                try:
                    url_title = google_scrape(url)
                except AttributeError:
                    url_title = ''
                print('url title ', url_title)
                urls.append({
                    'url_title': url_title,
                    'url': url,
                    'query': paper_title,
                })
        with open('./papers/query_urls.json', 'w') as f_out:
            json.dump(urls, f_out, indent=4, sort_keys=True)
        return urls

    @staticmethod
    def download(urls, target_dir):
        """Download urls to target_dir"""
        pass

    @staticmethod
    def extract_and_combine(source_dir):
        pass

    def process(self):
        paper_titles = self.get_paper_titles(self.config.paper_list_txt)
        urls = self.get_arxiv_urls(paper_titles)
        self.download(urls, self.config.dl_dir)
        self.extract_and_combine(self.config.dl_dir)


if __name__ == '__main__':
    config = FileDownloadAndCombinerConfig()
    downloader = FileDownloadAndCombiner(config=config)
    downloader.process()
