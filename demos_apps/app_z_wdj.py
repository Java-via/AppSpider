# _*_ coding: utf-8 _*_

"""
comprehensive and main for wdj
"""

import logging
import datetime
import collections
import urllib.request
import bs4
import spider
from .app_fetcher import FetcherWDJ
from .app_parser import Parser
from .app_saver import UpdateSaver


def get_wdj_index():
    """
    get index data
    """
    url_soft = "http://www.wandoujia.com/category/app"
    url_game = "http://www.wandoujia.com/category/game"

    index_data_soft = []
    index_data_game = []
    classify = collections.defaultdict(list)

    for url in [url_soft, url_game]:
        response = urllib.request.urlopen(url, timeout=10)
        soup = bs4.BeautifulSoup(spider.get_html_content(response), "html.parser")

        ul_soup = soup.find("ul", class_="clearfix tag-box")
        for li_soup in ul_soup.find_all("li", class_="parent-cate"):
            first_level_a = li_soup.find("a", class_="cate-link")
            first_level_url = spider.get_url_legal(first_level_a.get("href"), base_url="http://www.wandoujia.com/")
            first_level_tag = first_level_a.get("title")
            if url == url_soft:
                index_data_soft.append((1, (first_level_tag,), first_level_url))
            else:
                index_data_game.append((1, (first_level_tag,), first_level_url))

            for second_level_a in li_soup.find_all("a", class_=None):
                second_level_url = spider.get_url_legal(second_level_a.get("href"),
                                                        base_url="http://www.wandoujia.com/")
                second_level_tag = second_level_a.get("title")
                if url == url_soft:
                    index_data_soft.append((2, (first_level_tag, second_level_tag), second_level_url))
                else:
                    index_data_game.append((2, (first_level_tag, second_level_tag), second_level_url))

                classify[first_level_tag].append(second_level_tag)
    assert len(index_data_soft) > 0 and len(index_data_game) > 0, "get index error"

    logging.warning("get_wdj_index: len(soft)=%s, len(game)=%s", len(index_data_soft), len(index_data_game))
    for item in index_data_soft + index_data_game:
        logging.warning(str(item))

    return index_data_soft, index_data_game, classify


def main_wdj():
    """
    main function
    """
    log_file = "wdj_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file, filemode="w")

    index_data_soft, index_data_game, classify = get_wdj_index()
    web_spider = spider.WebSpiderT(FetcherWDJ(classify), Parser(), UpdateSaver(source="wdj"), url_filter=spider.UrlFilter(black_patterns=[]))

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
