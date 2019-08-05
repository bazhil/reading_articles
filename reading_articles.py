import urllib.request
import re
from config import *

def extract_article(url):
    """
    Function, which extract article from web page
    :param url:
    :return:
    """
    # read page
    response = urllib.request.urlopen(url)
    article = response.read().decode('utf-8')

    # get title of article
    title = article.split(title_start_tag)[1].split(title_finish_tag)[0].replace('&nbsp;', ' ')

    # get text of article
    text = article.split(text_start_tag)[1].split(text_finish_tag)[0]
    text = text.replace('<p>', '')
    text = text.replace('</p>', '\n\n')
    text = text.replace('<i>', '').replace('</i>', '')
    text = text.replace('<a href="', '[').replace('" target="_blank">', '] ').replace('</a>', '')
    words = text.split(' ')

    # purify text
    for i in words:
        if i.startswith('['):
            if re.search(r'(https?://[^\s]+)', i):
                pass
            else:
                words.remove(i)

    #
    publication = '' + title + '\n\n'
    line = ''
    for word in words:
        if (len(line) + len(word)) >= 81:
            publication += line + '\n'
            line = ''
            line += word + ' '
        else:
            line += word + ' '

    # write text in .txt
    with open('{}.txt'.format(title), 'w') as output_file:
        output_file.write(publication)

extract_article(url)