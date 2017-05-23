# _*_ coding: utf-8 _*_

"""
comprehensive and main for yyb
"""

import logging
import datetime
import collections
import urllib.request
import bs4
import spider
from .app_fetcher import FetcherYYB
from .app_parser import Parser
from .app_saver import UpdateSaver


def get_yyb_index():
    """
    get index data
    """
    url_soft = "http://sj.qq.com/myapp/category.htm?orgame=1"
    url_game = "http://sj.qq.com/myapp/category.htm?orgame=2"

    index_data_soft = []
    index_data_game = []
    classify = collections.defaultdict(list)

    for url in [url_soft, url_game]:
        response = urllib.request.urlopen(url, timeout=5)
        soup = bs4.BeautifulSoup(spider.get_html_content(response), "html.parser")

        ul_soup = soup.find("ul", class_="menu-junior")
        for a_soup in ul_soup.find_all("a"):
            this_url = a_soup.get("href")
            if this_url.find("javascript") >= 0:
                continue
            if this_url.find("categoryId") < 0:
                this_url += "&categoryId=0"
            this_tags = (a_soup.get_text(),) if not a_soup.get_text().strip().startswith("全部") else tuple()

            if url == url_soft:
                index_data_soft.append((1 if len(this_tags) == 0 else 2, this_tags, this_url))
            else:
                index_data_game.append((1 if len(this_tags) == 0 else 2, this_tags, this_url))

            if len(this_tags) > 0:
                classify[this_tags[0]] = []
    assert len(index_data_soft) > 0 and len(index_data_game) > 0, "get index error"

    logging.warning("get_yyb_index: len(soft)=%s, len(game)=%s", len(index_data_soft), len(index_data_game))
    for item in index_data_soft + index_data_game:
        logging.warning((str(item)))

    return index_data_soft, index_data_game, classify


def main_yyb():
    """
    main function
    """
    log_file = "yyb_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file, filemode="w")
    _url = "http://sj.qq.com/myapp/cate/appList.htm"

    index_data_soft, index_data_game, classify = get_yyb_index()
    web_spider = spider.WebSpiderT(FetcherYYB(classify), Parser(), UpdateSaver(source="yyb"), url_filter=spider.UrlFilter(black_patterns=[]))

    for level, tags, url in index_data_soft:
        if level == 2:
            web_spider.set_start_url(_url+url+"&pageSize=20", ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 2:
            web_spider.set_start_url(_url+url+"&pageSize=20", ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=False)

    for level, tags, url in index_data_soft:
        if level == 1:
            web_spider.set_start_url(_url+url+"&pageSize=20", ("soft", tags, "index"), priority=0, deep=0, critical=True)
    for level, tags, url in index_data_game:
        if level == 1:
            web_spider.set_start_url(_url+url+"&pageSize=20", ("game", tags, "index"), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=True)
    return
