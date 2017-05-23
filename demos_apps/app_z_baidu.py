# _*_ coding: utf-8 _*_

"""
comprehensive and main for baidu
"""

import re
import logging
import datetime
import collections
import urllib.request
import bs4
import spider
from .app_fetcher import FetcherBaidu
from .app_parser import Parser
from .app_saver import UpdateSaver


def get_baidu_index():
    """
    get index data
    """
    url_soft = "http://shouji.baidu.com/software/"
    url_game = "http://shouji.baidu.com/game/"

    index_data_soft = []
    index_data_game = []
    classify = collections.defaultdict(list)

    for url in [url_soft, url_game]:
        response = urllib.request.urlopen(url, timeout=10)
        soup = bs4.BeautifulSoup(spider.get_html_content(response, charset="utf-8"), "html.parser")

        ul_soup = soup.find("ul", class_="cate")
        for li_soup in ul_soup.find_all("li", class_=re.compile(r"^cate-item")):
            first_level_tag = None
            for a_soup in li_soup.find_all("a"):
                this_url = spider.get_url_legal(a_soup.get("href"), base_url="http://shouji.baidu.com/")
                if not first_level_tag:
                    this_tags = (a_soup.get_text(),)
                    first_level_tag = a_soup.get_text()
                else:
                    this_tags = (first_level_tag, a_soup.get_text())
                    classify[first_level_tag].append(a_soup.get_text())

                if url == url_soft:
                    index_data_soft.append((1 if this_url.find("board") <= 0 else 2, this_tags, this_url))
                else:
                    index_data_game.append((1 if this_url.find("board") <= 0 else 2, this_tags, this_url))
    assert len(index_data_soft) > 0 and len(index_data_game) > 0, "get index error"

    logging.warning("get_baidu_index: len(soft)=%s, len(game)=%s", len(index_data_soft), len(index_data_game))
    for item in index_data_soft + index_data_game:
        logging.warning(str(item))

    return index_data_soft, index_data_game, classify


def main_baidu():
    """
    main function
    """
    log_file = "baidu_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file, filemode="w")

    index_data_soft, index_data_game, classify = get_baidu_index()
    web_spider = spider.WebSpiderT(FetcherBaidu(classify), Parser(), UpdateSaver(source="baidu"), url_filter=spider.UrlFilter(black_patterns=[]))

    for level, tags, url in index_data_soft:
        if level == 2:
            web_spider.set_start_url(url, ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 2:
            web_spider.set_start_url(url, ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(is_over=False)

    for level, tags, url in index_data_soft:
        if level == 1:
            web_spider.set_start_url(url, ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 1:
            web_spider.set_start_url(url, ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(is_over=True)
    return
