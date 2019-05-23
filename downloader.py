from tqdm import tqdm
from fuzzywuzzy import fuzz
import os
from utils.scrape import download
from utils.scrape import get_arxiv_urls
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
    def filter_valid_urls(urls):
        valid_url_list = []
        for data in urls:
            str1 = data['title'].lower()
            str2 = data['url_title'].lower()
            ratio = fuzz.ratio(str1, str2)
            # need manual screening to get this threshold
            if ratio < 70:
                # print('score', ratio)
                # print(str1)
                # print(str2)
                # print('-=-=')
                continue
            else:
                valid_url_list.append(data)
        return valid_url_list

    @staticmethod
    def download(urls, target_dir):
        """Download urls to target_dir

        Args:
            urls: list of dict with keys 'url', 'url_title', 'title'
            target_dir:

        Returns:

        """
        valid_urls = FileDownloadAndCombiner.filter_valid_urls(urls)
        print('Downloading {} papers'.format(len(valid_urls)))
        for data in tqdm(valid_urls[:]):
            url = data['url'].replace('abs', 'pdf') + '.pdf'
            filename = os.path.join(target_dir, data['title'] + '.pdf')
            filename = filename.replace('"', '').replace('/', '')
            print(url)
            print(filename)
            download(url, filename)

    @staticmethod
    def extract_and_combine(source_dir):
        batch_extract_from_folder(source_pdf_dir=source_dir, output_pdf_dir=source_dir)

    def process(self):
        paper_titles = self.get_paper_titles(self.config.paper_list_txt)
        urls = get_arxiv_urls(paper_titles)
        self.download(urls, self.config.dl_dir)
        self.extract_and_combine(self.config.dl_dir)


if __name__ == '__main__':
    config = FileDownloadAndCombinerConfig()
    downloader = FileDownloadAndCombiner(config=config)
    downloader.process()
