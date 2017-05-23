# _*_ coding: utf-8 _*_

import sys
import spider
import logging
import urllib.request
logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")


def test_urlfilter():
    """
    test urlfilter
    """
    url_list = ["http://baidu.com/", "http://baidu.com/1", "http://baidu.com/2", "http://baidu.com/1", "http://test.com"]
    url_filter_1 = spider.UrlFilter(capacity=None)
    url_filter_2 = spider.UrlFilter(capacity=10)
    for url in url_list:
        print(url, url_filter_1.check(url), url_filter_2.check(url))
    return


def test_yundama():
    """
    test yundama
    """
    ydm = spider.YunDaMa("qixianhu", "mimaMIMA123456")
    file_bytes = urllib.request.urlopen("http://www.yundama.com/index/captcha").read()
    cid, code = ydm.get_captcha(file_bytes, "captcha.jpeg", "image/jpeg", codetype="1000", repeat=10)
    print(cid, code)
    if cid and (not code):
        ydm.result(cid)
    return


def test_spider(mysql, spider_type):
    """
    test spider
    """
    fetcher = spider.Fetcher(normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=5, critical_sleep_time=5)
    parser = spider.Parser(max_deep=1, max_repeat=3)

    if not mysql:
        saver = spider.Saver(save_pipe=sys.stdout)
        url_filter = spider.UrlFilter(
            black_patterns=(spider.CONFIG_URLPATTERN_FILES, r"/binding$"),
            white_patterns=("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360)|duba_\d)\.(com|cn)", ),
            capacity=None
        )
    else:
        saver = spider.SaverMysql(host="101.200.174.172", user="dba_0", passwd="mimadba_0", database="data_secret")
        saver.change_sqlstr("insert into t_test(url, title, getdate) values (%s, %s, %s);")
        url_filter = spider.UrlFilter(
            black_patterns=(spider.CONFIG_URLPATTERN_FILES, r"/binding$"),
            white_patterns=("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360)|duba_\d)\.(com|cn)", ),
            capacity=1000
        )

    if spider_type == "thread":
        web_spider = spider.WebSpiderT(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)
    else:
        web_spider = spider.WebSpiderP(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)

    parser_num = 1 if spider_type == "thread" else 3
    web_spider.set_start_url("http://www.wandoujia.com/apps", ("wandoujia",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=5, parser_num=parser_num, is_over=False)

    web_spider.set_start_url("http://zhushou.360.cn/", ("360app",), priority=0, deep=0, critical=False)
    for i in range(5):
        web_spider.set_start_url("https://www.duba_%d.com/" % i, ("critical",), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=5, parser_num=parser_num, is_over=True)
    return


if __name__ == '__main__':
    # test_urlfilter()
    # test_yundama()

    # test_spider(mysql=False, spider_type="thread")
    test_spider(mysql=True, spider_type="thread")

    # test_spider(mysql=False, spider_type="process")
    test_spider(mysql=True, spider_type="process")
    exit()
