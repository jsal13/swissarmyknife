# import re

import requests as req
from bs4 import BeautifulSoup

URLS = [
    "https://use-the-index-luke.com/sql/preface",
    "https://use-the-index-luke.com/sql/anatomy",
    "https://use-the-index-luke.com/sql/anatomy/the-leaf-nodes",
    "https://use-the-index-luke.com/sql/anatomy/the-tree",
    "https://use-the-index-luke.com/sql/anatomy/slow-indexes",
    "https://use-the-index-luke.com/sql/where-clause",
    "https://use-the-index-luke.com/sql/where-clause/the-equals-operator",
    "https://use-the-index-luke.com/sql/where-clause/the-equals-operator/primary-keys",
    "https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys",
    "https://use-the-index-luke.com/sql/where-clause/the-equals-operator/slow-indexes-part-ii",
    "https://use-the-index-luke.com/sql/where-clause/functions",
    "https://use-the-index-luke.com/sql/where-clause/functions/case-insensitive-search",
    "https://use-the-index-luke.com/sql/where-clause/functions/user-defined-functions",
    "https://use-the-index-luke.com/sql/where-clause/functions/over-indexing",
    "https://use-the-index-luke.com/sql/where-clause/bind-parameters",
    "https://use-the-index-luke.com/sql/where-clause/searching-for-ranges",
    "https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/greater-less-between-tuning-sql-access-filter-predicates",
    "https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/like-performance-tuning",
    "https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/index-merge-performance",
    "https://use-the-index-luke.com/sql/where-clause/partial-and-filtered-indexes",
    "https://use-the-index-luke.com/sql/where-clause/null",
    "https://use-the-index-luke.com/sql/where-clause/null/index",
    "https://use-the-index-luke.com/sql/where-clause/null/not-null-constraint",
    "https://use-the-index-luke.com/sql/where-clause/null/partial-index",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation/dates",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation/numeric-strings",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation/concatenation",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation/smart-logic",
    "https://use-the-index-luke.com/sql/where-clause/obfuscation/math",
    "https://use-the-index-luke.com/sql/testing-scalability",
    "https://use-the-index-luke.com/sql/testing-scalability/data-volume",
    "https://use-the-index-luke.com/sql/testing-scalability/system-load",
    "https://use-the-index-luke.com/sql/testing-scalability/response-time-throughput-scaling-horizontal",
    "https://use-the-index-luke.com/sql/join",
    "https://use-the-index-luke.com/sql/join/nested-loops-join-n1-problem",
    "https://use-the-index-luke.com/sql/join/hash-join-partial-objects",
    "https://use-the-index-luke.com/sql/join/sort-merge-join",
    "https://use-the-index-luke.com/sql/clustering",
    "https://use-the-index-luke.com/sql/clustering/index-filter-predicates",
    "https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index",
    "https://use-the-index-luke.com/sql/clustering/index-organized-clustered-index",
    "https://use-the-index-luke.com/sql/sorting-grouping",
    "https://use-the-index-luke.com/sql/sorting-grouping/indexed-order-by",
    "https://use-the-index-luke.com/sql/sorting-grouping/order-by-asc-desc-nulls-last",
    "https://use-the-index-luke.com/sql/sorting-grouping/indexed-group-by",
    "https://use-the-index-luke.com/sql/partial-results",
    "https://use-the-index-luke.com/sql/partial-results/top-n-queries",
    "https://use-the-index-luke.com/sql/partial-results/fetch-next-page",
    "https://use-the-index-luke.com/sql/partial-results/window-functions",
    "https://use-the-index-luke.com/sql/dml",
    "https://use-the-index-luke.com/sql/dml/insert",
    "https://use-the-index-luke.com/sql/dml/delete",
    "https://use-the-index-luke.com/sql/dml/update",
]


def make_soup(url: str) -> BeautifulSoup:
    """Get html from URL, return Soup."""
    resp: str = req.get(url=url).content
    return BeautifulSoup(resp, features="html.parser")


# def replace_image_url(article_html: str) -> str:
#     """Put URL back into image a href."""
#     pattern: str = r"/wp-content/uploads"
#     repl: str = r"https://www.annemini.com/wp-content/uploads"
#     return re.sub(pattern, repl, article_html)


soup = [make_soup(url=url) for url in URLS]
content = [
    str(soup_item.find_all("div", {"class": "content"})[0]) for soup_item in soup
]
html = "<html><head></head><body>" + "\n".join(content) + "</body></html>"

with open("ebook.html", "w+") as f:
    f.write(html)

# Now go to Calibre and convert to HTML.
