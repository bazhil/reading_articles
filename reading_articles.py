import urllib.request
import re
from config import *

class Extract_article():
    """
    Class, which extract article from web page (only lenta.ru now)
    :param url:
    :return:
    """
    def __init__(self):
        self.url = url
        self.title_start_tag = title_start_tag
        self.title_finish_tag = title_finish_tag
        self.text_start_tag = text_start_tag
        self.text_finish_tag = text_finish_tag
        self.article = ''
        self.title = ''
        self.text = ''
        self.words = []
        self.publication = ''


    def read_page(self):
        """
        Function which get html from page
        :return:
        """
        response = urllib.request.urlopen(self.url)
        self.article = response.read().decode('utf-8')


    def get_title(self):
        """
        Function, which get title text
        :return:
        """
        self.title = self.article.split(title_start_tag)[1].split(title_finish_tag)[0].replace('&nbsp;', ' ')

    def get_text(self):
        """
        Function, which get text
        :return:
        """
        self.text = self.article.split(text_start_tag)[1].split(text_finish_tag)[0]
        self.text = self.text.replace('<p>', '')
        self.text = self.text.replace('</p>', '\n\n')
        self.text = self.text.replace('<i>', '').replace('</i>', '')
        self.text = self.text.replace('<a href="', '[').replace('" target="_blank">', '] ').replace('</a>', '')
        self.words = self.text.split(' ')

    def purify_text(self):
        """
        Clean text from local lincs
        :return:
        """
        for i in self.words:
            if i.startswith('['):
                if re.search(r'(https?://[^\s]+)', i):
                    pass
                else:
                    self.words.remove(i)

    def format_text(self):
        """
        Format text
        :return:
        """
        self.publication = '' + self.title + '\n\n'
        line = ''
        for word in self.words:
            if (len(line) + len(word)) >= 81:
                self.publication += line + '\n'
                line = ''
                line += word + ' '
            else:
                line += word + ' '
        self.publication += line + '\n'


    def write_text(self):
        """
        Function, which write text to txt-file
        :return:
        """
        with open('{}.txt'.format(self.title), 'w') as output_file:
            output_file.write(self.publication)

    def parse(self):
        """
        Function, which parse web-page
        :return:
        """
        self.read_page()
        self.get_title()
        self.get_text()
        self.purify_text()
        self.format_text()
        self.write_text()

if __name__ == '__main__':
    parser = Extract_article()
    parser.parse()