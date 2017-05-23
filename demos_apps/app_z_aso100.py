# _*_ coding: utf-8 _*_

"""
comprehensive and main for aso100
"""

import collections
import urllib.request
import bs4
import spider
import logging
import datetime
from .app_fetcher import FetcherASO
from .app_parser import Parser
from .app_saver import UpdateSaver


def get_aso_index():
    """
    get index data
    """
    url_list = [
        "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/36",
        "http://aso100.com/rank/index/device/iphone/country/cn/brand/paid/genre/36",
        "http://aso100.com/rank/index/device/iphone/country/cn/brand/grossing/genre/36",
    ]

    index_data = []
    classify = collections.defaultdict(list)
    for url in url_list:
        response = urllib.request.urlopen(url, timeout=10)
        soup = bs4.BeautifulSoup(spider.get_html_content(response), "html.parser")
        ul_soup = soup.find("ul", class_="dropdown-menu wide dropdown-menu-mobile")
        for li_soup in ul_soup.find_all("li", recursive=False):
            if li_soup.get("class") and li_soup.get("class")[0] == "cascade":
                a_soup = li_soup.find("a")
                this_url = spider.get_url_legal(a_soup.get("href"), "http://aso100.com/")
                this_tag_first = a_soup.get_text().strip()
                index_data.append((1, (this_tag_first, ), this_url))

                ul_soup_temp = li_soup.find("ul", class_="cascade-menu dropdown-menu")
                for li_soup_temp in ul_soup_temp.find_all("li", recursive=False):
                    a_soup = li_soup_temp.find("a")
                    this_url = spider.get_url_legal(a_soup.get("href"), "http://aso100.com/")
                    this_tag_second = a_soup.get_text().strip()
                    index_data.append((1, (this_tag_first, this_tag_second), this_url))
            else:
                a_soup = li_soup.find("a")
                this_url = spider.get_url_legal(a_soup.get("href"), "http://aso100.com/")
                this_tag_first = a_soup.get_text()
                index_data.append((1, (this_tag_first, ), this_url))

    for item in index_data:
        logging.warning(str(item))

    return index_data, classify


def main_aso():
    """
    main function
    """
    log_file = "aso_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file, filemode="w")

    index_data, classify = get_aso_index()
    web_spider = spider.WebSpiderT(FetcherASO(classify), Parser(), UpdateSaver("", is_update=False))

    for level, tags, url in index_data:
        keys = (",".join(url.split("/")[6:13:2]), tags, 0, "index")
        web_spider.set_start_url(url, keys, priority=0, deep=0, critical=True)
        web_spider.start_work_and_wait_done(is_over=True)
    return
