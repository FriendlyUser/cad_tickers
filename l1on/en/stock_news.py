import requests
import bs4
import pandas as pd
from typing import List, Union, Tuple
from concurrent.futures import ThreadPoolExecutor


def scrap_news_for_ticker(ticker: str) -> List[dict]:
    """Extracts webpage data from a ticker

    TODO add a delay

    Parameters:
      ticker - yahoo finance ticker
    Returns:
      news_data - list of dicts extracted from webpage
        * source - str
        * link_href - link from post (can be relative or absolute)
        * link_text - description for link
        * ticker - reference to original ticker

    """
    try:
        yahoo_base_url = "https://finance.yahoo.com"
        news_items, html_content = get_ynews_for_ticker(ticker, yahoo_base_url)
        news_data = []
        for news_item in news_items:
            # remove comments
            for comment in news_item(text=lambda text: isinstance(text, bs4.Comment)):
                comment.extract()
            # grab description header, stuff next too image
            news_content = news_item.find(
                "div", {"class": "Ov(h) Pend(44px) Pstart(25px)"}
            )
            if news_content is None:
                # try again with different class
                news_content = news_item.find("div", {"class": "Ov(h)"})
            source = find_news_source(news_content)
            link_href, link_text = find_news_link_and_text(news_content)
            news_data.append(
                {
                    "source": source,
                    "link_href": link_href,
                    "link_text": link_text,
                    "ticker": ticker,
                }
            )
        return news_data
    except Exception as e:
        print(e)
        return []


def get_ynews_for_ticker(
    ticker: str, yahoo_base_url="https://finance.yahoo.com"
) -> List[bs4.element.Tag]:
    """Returns initial news items fetched from yahoo when loading quote page.
    Since yahoo has lazy loading, not all items are returned. Seems like ads are not loaded
    because of lazy loading.

      Parameters:
        ticker - yahoo formatted ticker str
        yahoo_base_url - optional parameter that is the base of the request

      Returns:
        news_items - list of key html content for the news item
    """
    yahoo_qurl = f"{yahoo_base_url}/quote/{ticker}?p={ticker}"
    r = requests.get(yahoo_qurl)
    html_content = r.text
    soup = bs4.BeautifulSoup(html_content, "lxml")
    news_items = soup.find_all(
        "li", {"class": "js-stream-content Pos(r)"}
    )  # This will return a list of all line items in the markup.
    return news_items, html_content


def find_news_link_and_text(news_content: bs4.element.Tag) -> Tuple[str, str]:
    """Finds news link from news_content.
       Assumes comments are deleted from the yahoo finance news items

    Parameters:
      news_content - html based data for the news article

    Returns:
      link_href - link in html markup
      link_text - link text in html markup
    """
    if news_content is None:
        return "", ""
    link_tag = news_content.find("a")
    link_href = link_tag.get("href")
    link_text = link_tag.text
    return link_href, link_text


def find_news_source(news_content: bs4.element.Tag) -> Union[None, str]:
    """Utility function to verify news format from yahoo has not changed

    when grabbing data from yahoo with requests, it seems date is not returned.

    Parameters:
      news_content: html based data for the news article

    Returns:
      source - publisher of article

    wrapper div around content - such as - CNW Group 2 days ago
    """
    if news_content is None:
        return
    # wrapper div around content - such as - CNW Group 2 days ago
    wrapper_div = news_content.find(
        "div", {"class": "C(#959595) Fz(11px) D(ib) Mb(6px)"}
    )
    source = wrapper_div.text
    return source


if __name__ == "__main__":
    scrap_news_for_ticker("IP.CN")
