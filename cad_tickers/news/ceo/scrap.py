import requests
import bs4
from bs4 import BeautifulSoup   
from cad_tickers.news.ceo.utils import module_logger

def extract_article(article_url: str)-> bs4.element.Tag:
    """Extracts data from given ceo news url"""
    r = requests.get(article_url)
    if r == None:
        module_logger.warning('No data returned from the url')
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    try:
        scripts = [x.extract() for x in soup.findAll('script')]
    except AttributeError as e:
        module_logger.warning('No Scripts to Extract from article')
    # print(soup.prettify())
    article = soup.find(attrs={'class': 'article-body article'})
    # Use this as a example
    # remove image tags
    if article == None:
        article = soup.find(id='article')
    if article == None:
        article = soup.find(id='article-container')
    try:
        image_text = article.findAll(lambda tag : tag.name == 'span' and 'Click Image To View Full Size' in tag.text)
        [x.extract() for x in image_text]
    except AttributeError as e:
        module_logger.warning('No Click Image to View Full Size text')
    try:
        images = [x.extract() for x in soup.findAll('img')]
    except AttributeError as e:
        module_logger.warning('No Images in news report')
    return article

def save_bs4_tag(tag: bs4.element.Tag, file_name: str=''):
    """Save bs4 tag to file"""
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(tag.text)

if __name__ == '__main__':
    pass