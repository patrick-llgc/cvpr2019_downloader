import os
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
            paper_titles = f_in.readlines()[1:]
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