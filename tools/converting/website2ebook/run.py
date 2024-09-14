import re

import requests as req
from bs4 import BeautifulSoup

URLS = [
    "https://www.annemini.com/category/start-here-if-you-are-a-beginner-at-trying-to-get-published/"
]


def make_soup(url: str) -> BeautifulSoup:
    """Get html from URL, return Soup."""
    resp: str = req.get(url=url).content
    return BeautifulSoup(resp)


def replace_image_url(article_html: str) -> str:
    """Put URL back into image a href."""
    pattern: str = r"/wp-content/uploads"
    repl: str = r"https://www.annemini.com/wp-content/uploads"
    return re.sub(pattern, repl, article_html)


soup = make_soup(url=URLS[0])
articles = [
    replace_image_url(article_html=str(article_html))
    for article_html in soup.find_all("article")
]

html = "<html><head></head><body>" + "\n".join(articles) + "</body></html>"

with open("ebook.html", "w+") as f:
    f.write(html)

# Now go to Calibre and convert to HTML.
