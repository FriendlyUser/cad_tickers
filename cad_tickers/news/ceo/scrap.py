import requests
import bs4
from bs4 import BeautifulSoup   

def extract_article(article_url: str)-> bs4.element.Tag:
    """Extracts data from given ceo news url"""
    r = requests.get(article_url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    scripts = [x.extract() for x in soup.findAll('script')]
    # print(soup.prettify())
    article = soup.find(attrs={'class': 'article-body article'})
    # remove image tags
    try:
        image_text = article.findAll(lambda tag : tag.name == 'span' and 'Click Image To View Full Size' in tag.text)
        [x.extract() for x in image_text]
        images = [x.extract() for x in soup.findAll('img')]
    except AttributeError as e:
        print(e)
    return article

def save_bs4_tag(tag: bs4.element.Tag, file_name: str=''):
    """Save bs4 tag to file"""
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(tag.text)

if __name__ == '__main__':
    pass