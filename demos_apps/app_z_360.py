# _*_ coding: utf-8 _*_

"""
comprehensive and main for 360
"""

import logging
import datetime
import collections
import urllib.request
import bs4
import spider
from .app_fetcher import Fetcher360
from .app_parser import Parser
from .app_saver import UpdateSaver


def get_360_index():
    """
    get index data
    """
    url_soft = "http://zhushou.360.cn/list/index/cid/1/"
    url_game = "http://zhushou.360.cn/list/index/cid/2/"

    index_data_soft = []
    index_data_game = []
    classify = collections.defaultdict(list)

    for url in [url_soft, url_game]:
        response = urllib.request.urlopen(url, timeout=10)
        soup = bs4.BeautifulSoup(spider.get_html_content(response), "html.parser")
        ul_soup = soup.find("ul", class_="select")
        for a_soup in ul_soup.find("li").find_all("a"):
            this_url = spider.get_url_legal(a_soup.get("href"), base_url="http://zhushou.360.cn/")
            this_tags = (a_soup.get_text(),) if a_soup.get_text().strip() != "全部" else tuple()

            if url == url_soft:
                index_data_soft.append((1 if len(this_tags) == 0 else 2, this_tags, this_url))
            else:
                index_data_game.append((1 if len(this_tags) == 0 else 2, this_tags, this_url))

            if len(this_tags) > 0:
                classify[this_tags[0]] = []
    assert len(index_data_soft) > 0 and len(index_data_game) > 0, "get index error"

    logging.warning("get_360_index: len(soft)=%s, len(game)=%s", len(index_data_soft), len(index_data_game))
    for item in index_data_soft + index_data_game:
        logging.warning(str(item))

    return index_data_soft, index_data_game, classify


def main_360():
    """
    main function
    """
    log_file = "360_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file, filemode="w")

    index_data_soft, index_data_game, classify = get_360_index()
    web_spider = spider.WebSpiderT(Fetcher360(classify), Parser(), UpdateSaver(source="360"), url_filter=spider.UrlFilter(black_patterns=[]))

    for level, tags, url in index_data_soft:
        if level == 2:
            web_spider.set_start_url(url, ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 2:
            web_spider.set_start_url(url, ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=False)

    for level, tags, url in index_data_soft:
        if level == 1:
            web_spider.set_start_url(url, ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 1:
            web_spider.set_start_url(url, ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=True)
    return
