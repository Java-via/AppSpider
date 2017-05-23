# _*_ coding: utf-8 _*_

"""
fetcher for 360, baidu, wdj, yyb, aso100
"""

import re
import json
import datetime
import urllib.request
import bs4
import spider
from .app_config import App


class FetcherApp(spider.Fetcher):
    """
    basic fetcher for apps
    """

    def __init__(self, classify, normal_max_repeat=5, normal_sleep_time=5, critical_max_repeat=100, critical_sleep_time=60):
        spider.Fetcher.__init__(self, normal_max_repeat, normal_sleep_time, critical_max_repeat, critical_sleep_time)
        self.classify = classify
        self.classifystring = "视频音乐购物阅读导航社交摄影新闻工具美化教育生活安全旅游儿童理财系统健康娱乐办公通讯出行"
        return

    def url_fetch(self, url, keys, critical, repeat):
        """
        fetch the content of a url
        """
        headers = spider.make_headers(user_agent="pc", accept_encoding="gzip, deflate")
        response = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10)
        content = self.htm_parse(url, keys, spider.get_html_content(response, charset="utf-8"))
        return 1, content

    def htm_parse(self, url, keys, cur_html):
        """
        html parser, return url_list, save_list
        """
        raise NotImplementedError


class Fetcher360(FetcherApp):
    """
    class of Fetcher360
    """

    def htm_parse(self, url, keys, cur_html):
        """
        html parser, return url_list, save_list
        :param keys: (soft/game, tags, index/item)
        """
        url_list, save_list = [], []
        soup = bs4.BeautifulSoup(cur_html, "html.parser")

        if keys[-1] == "index":
            for li_soup in soup.find("ul", class_="iconList").find_all("li"):
                this_url = spider.get_url_legal(li_soup.find("a").get("href"), base_url="http://zhushou.360.cn/")
                url_list.append((this_url, (keys[0], keys[1], "item"), False, 0))

            if (url.find("list/index/cid/") > 0) and (url.find("?page=") < 0):
                for i in range(2, 51):
                    url_list.append((url + ("?page=%d" % i), (keys[0], keys[1], "index"), True, 1))

        elif keys[-1] == "item":
            json_data = spider.get_json_data(cur_html, pattern="return\s+?(?P<i>\{[\w\W]+?\})")
            assert json_data, "json_data is null"

            app = App(softgame=keys[0], url=url, source="360")

            app.a_pkgname = json_data["pname"]
            app.a_name = json_data["sname"]
            app.a_classify = ",".join(keys[1])

            _image_soup = soup.find("img", width=True, height=True, alt=True)
            assert _image_soup, "_image_soup is null"
            app.a_picurl = _image_soup.get("src")

            _info_soup = soup.find("div", class_="base-info")
            assert _info_soup, "_info_soup is null"
            text_list = [spider.get_string_strip(item.get_text()) for item in _info_soup.find_all("td")]
            text_list = [item.split("：") for item in text_list]
            app.a_publisher = spider.get_string_strip(text_list[0][1])
            app.a_updatedate = datetime.datetime.strptime(text_list[1][1], "%Y-%m-%d")
            app.a_version = spider.get_string_strip(text_list[2][1])

            _desc_soup = soup.find("div", class_=re.compile(r"(breif|html-brief)"))
            assert _desc_soup, "_desc_soup is null"
            text = _desc_soup.get_text()
            end_index = text.find("【基本信息】")
            if end_index > 0:
                text = text[:end_index]
            app.a_description = text.strip()

            _tags_soup = soup.find("div", class_="app-tags")
            app.a_defaulttags = ",".join([a.get_text().strip() for a in _tags_soup.find_all("a")]) if _tags_soup else ""

            _count_soup = soup.find("div", class_="pf")
            assert _count_soup, "_count_soup is null"
            count_list = [item.get_text() for item in _count_soup.find_all("span")]
            app.a_score = spider.get_string_num(count_list[0])
            app.a_install = int(spider.get_string_num(count_list[-2]))
            app.a_bytes = int(spider.get_string_num(count_list[-1], base=1024))

            save_list.append(app)
        return 1, url_list, save_list


class FetcherBaidu(FetcherApp):
    """
    class of FetcherBaidu
    """

    def htm_parse(self, url, keys, cur_html):
        """
        parse the content of a url
        :param keys: (soft/game, tags, index/item)
        :return url_list, save_list: [(url1, keys1, priority1), ...], [item1, item2, ...]
        """
        url_list, save_list = [], []
        soup = bs4.BeautifulSoup(cur_html, "html.parser")

        if keys[-1] == "index":
            div_item = soup.find("div", class_="app-bd")
            for div_item in div_item.find_all("ul"):
                li_item = div_item.find_all("li")
                for li_item_item in li_item:
                    a_item = li_item_item.find("a")
                    this_url = spider.get_url_legal(a_item.get("href"), base_url="http://shouji.baidu.com/")
                    this_item = a_item.find("span", class_="inst-btn-big quickdown")
                    url_list.append((this_url, (keys[0], (keys[1], this_item), "item"), False, 0))

            li_soup = soup.find("div", class_="pager").find("li", class_="next")
            if li_soup:
                next_url = spider.get_url_legal(li_soup.find("a").get("href"), base_url=url)
                url_list.append((next_url, (keys[0], keys[1], "index"), True, 1))

        elif keys[-1] == "item":
            this_classify, this_item = keys[1]

            app = App(softgame=keys[0], url=url, source="baidu")

            app.a_pkgname = this_item.get("data_package")
            app.a_name = this_item.get("data_name")
            app.a_picurl = this_item.get("data_icon")

            app.a_bytes = int(spider.get_string_strip(this_item.get("data_size")))
            app.a_version = spider.get_string_strip(this_item.get("data_versionname"))

            app.a_classify = ":".join(this_classify)    # 注意这里是:分隔

            _detail_soup = soup.find("div", class_="detail")
            assert _detail_soup, "_detail_soup is null"
            _gold_soup = _detail_soup.find("span", class_="gold")
            app.a_publisher = _gold_soup.find_next_sibling().get_text().strip() if _gold_soup else ""
            app.a_install = int(spider.get_string_num(_detail_soup.find("span", class_="download-num").get_text()))

            _desc_soup = soup.find("div", class_="brief-long")
            assert _desc_soup, "_desc_soup is null"
            app.a_description = _desc_soup.get_text()

            _star_soup = soup.find("span", class_="star-percent")
            assert _star_soup, "_star_soup is null"
            app.a_score = spider.get_string_num(_star_soup.get("style"))

            save_list.append(app)
        return 1, url_list, save_list


class FetcherWDJ(FetcherApp):
    """
    class of FetcherWDJ
    """

    def htm_parse(self, url, keys, cur_html):
        """
        parse the content of a url
        :param keys: (soft/game, tags, index/item)
        :return url_list, save_list: [(url1, keys1, priority1), ...], [item1, item2, ...]
        """
        url_list, save_list = [], []
        soup = bs4.BeautifulSoup(cur_html, "html.parser")

        if keys[-1] == "index":
            for a_soup in soup.find_all("a", class_="name"):
                url_list.append((a_soup.get("href"), (keys[0], keys[1], "item"), False, 0))

            a_soup = soup.find("a", class_="page-item next-page ")
            if a_soup:
                next_url = a_soup.get("href")
                url_list.append((next_url, (keys[0], keys[1], "index"), True, 1))

        elif keys[-1] == "item":
            _info_soup = soup.find("div", class_="download-wp")
            assert _info_soup, "_info_soup is null"
            info = _info_soup.find("a")

            app = App(softgame=keys[0], url=url, source="wdj")

            app.a_pkgname = info.get("data-pn")
            app.a_name = info.get("data-name")

            _image_soup = soup.find("img", itemprop="image", alt=info.get("data-name"))
            assert _image_soup, "_image_soup is null"
            app.a_picurl = _image_soup.get("src")

            _infos_list_soup = soup.find("dl", class_="infos-list")
            assert _infos_list_soup, "_infos_list_soup is null"
            infos_list = [item.get_text() for item in _infos_list_soup.find_all("dd")]
            assert len(infos_list) == 7, "out of range, length=%d" % len(infos_list)

            a_classify = set(iter([":".join(keys[1])]))
            for item in spider.get_string_strip(infos_list[1]).split():
                for first_tag in self.classify:
                    if item in self.classify[first_tag]:
                        a_classify.add(":".join([first_tag, item]))
            app.a_classify = ",".join(a_classify)

            app.a_defaulttags = ",".join(spider.get_string_strip(infos_list[2]).split())
            app.a_bytes = int(spider.get_string_num(infos_list[0], base=1024))
            app.a_updatedate = datetime.datetime.strptime(infos_list[3].strip(), "%Y年%m月%d日")
            app.a_version = spider.get_string_strip(infos_list[4])
            app.a_publisher = spider.get_string_strip(infos_list[6])

            _subtitle_soup = soup.find("p", class_="tagline")
            assert _subtitle_soup, "_subtitle_soup is null"
            app.a_subtitle = spider.get_string_strip(_subtitle_soup.get_text())

            _desc_soup = soup.find("div", itemprop="description")
            assert _desc_soup, "_desc_soup is null"
            app.a_description = _desc_soup.get_text().strip()

            _account_soup = soup.find("div", class_="num-list")
            assert _account_soup, "_account_soup is null"
            account_list = [item.get_text() for item in _account_soup.find_all("i")]
            app.a_install = int(spider.get_string_num(account_list[0]))
            app.a_like = int(spider.get_string_num(account_list[1]))
            app.a_comment = int(spider.get_string_num(account_list[2]))

            save_list.append(app)
        return 1, url_list, save_list


class FetcherYYB(FetcherApp):
    """
    class of FetcherYYB
    """

    def htm_parse(self, url, keys, cur_html):
        """
        parse the content of a url
        :param keys: (soft/game, tags, index/item)
        :return url_list, save_list: [(url1, keys1, priority1), ...], [item1, item2, ...]
        """
        url_list, save_list = [], []

        if keys[-1] == "index":
            json_data = json.loads(cur_html)
            for this_item in json_data["obj"]:
                this_url = "http://sj.qq.com/myapp/detail.htm?apkName=%s" % this_item["pkgName"]
                url_list.append((this_url, (keys[0], "item"), False, 0))

            if json_data["count"] > 0 or len(url_list) > 0:
                if url.find("pageContext=") > 0:
                    _url, count = url[:url.rfind("=") + 1], url[url.rfind("=") + 1:]
                    this_url = _url + str(int(count) + 20)
                else:
                    this_url = url + "&pageContext=20"
                url_list.append((this_url, (keys[0], "index"), True, 1))

        elif keys[-1] == "item":
            json_data = spider.get_json_data(cur_html, pattern="appDetailData = (?P<item>\{[\w\W]+?\})", begin_pattern="\n\s+?")
            assert json_data, "json_data is null"
            soup = bs4.BeautifulSoup(cur_html, "html5lib")

            app = App(softgame=keys[0], url=url, source="yyb")

            app.a_name = json_data["appName"]
            app.a_pkgname = json_data["apkName"]
            app.a_picurl = json_data["iconUrl"]
            app.a_install = json_data["downTimes"]

            _infos_soup = soup.find_all("div", class_="det-othinfo-data")
            assert len(_infos_soup) >= 3, "_infos_soup is null"
            app.a_version = spider.get_string_strip(_infos_soup[0].get_text())
            app.a_updatedate = datetime.datetime.fromtimestamp(int(_infos_soup[1].get("data-apkpublishtime")))
            app.a_publisher = spider.get_string_strip(_infos_soup[2].get_text())

            _desc_soup = soup.find("div", class_="det-app-data-info")
            assert _desc_soup, "_desc_soup is null"
            app.a_description = _desc_soup.get_text().strip()

            _classify_soup = soup.find("a", class_="det-type-link")
            assert _classify_soup, "_classify_soup is null"
            app.a_classify = spider.get_string_strip(_classify_soup.get_text())
            if keys[0] == "unknown":
                app.a_softgame = "soft" if self.classifystring.find(app.a_classify) >= 0 else "game"

            _bytes_soup = soup.find("div", class_="det-size")
            assert _bytes_soup, "_bytes_soup is null"
            app.a_bytes = spider.get_string_num(_bytes_soup.get_text(), base=1024)

            _score_soup = soup.find("div", class_="com-blue-star-num")
            assert _score_soup, "_score_soup is null"
            app.a_score = _score_soup.get_text()[:-1]

            save_list.append(app)

            # 相关应用
            for li_soup in soup.find_all("li", class_="det-about-app-box"):
                this_url = spider.get_url_legal(li_soup.find("a").get("href"), base_url="http://sj.qq.com/myapp/")
                if this_url.rfind("&apkCode") > 0:
                    this_url = this_url[:this_url.rfind("&apkCode")]
                url_list.append((this_url, ("unknown", "item"), False, 0))

        return 1, url_list, save_list


class FetcherASO(FetcherApp):
    """
    class of FetcherASO
    """

    def __init__(self, classify):
        """
        constructor
        """
        FetcherApp.__init__(self, classify, critical_max_repeat=10, critical_sleep_time=60)
        cookie_string = "PHPSESSID=btqkg9amjrtoeev8coq0m78396; " \
                        "USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; " \
                        "Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1472528976; " \
                        "Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1472534045; " \
                        "ASOD=xyCtGMkg%2BeAQu4jGhbEHbwEv"
        self.cookiejar, self.opener = spider.make_cookiejar_opener()
        cookies_list = spider.make_cookies_string(cookie_string, domain="aso100.com")
        for cookie in cookies_list:
            self.cookiejar.set_cookie(cookie)
        return

    def url_fetch(self, url, keys, critical, repeat):
        """
        fetch the content of a url
        """
        headers = spider.make_headers(user_agent="pc", accept_encoding="gzip, deflate")
        response = self.opener.open(urllib.request.Request(url, headers=headers), timeout=10)
        content = self.htm_parse(url, keys, spider.get_html_content(response, charset="utf-8"))
        return 1, content

    def htm_parse(self, url, keys, cur_html):
        """
        parse the content of a url
        :return url_list, save_list: [(url1, keys1, critical priority1), ...], [item1, item2, ...]
        """
        url_list, save_list = [], []
        soup = bs4.BeautifulSoup(cur_html, "html5lib")

        # keys[0]:source   keys[1]:classify list   keys[2]:rank   keys[3]:index/detail
        if keys[-1] == "index":
            if url.find("/index/") >= 0:
                for page in range(2, 9):
                    more_url = url.replace("index", "more") + "?page=" + str(page)
                    url_list.append((more_url, (keys[0], keys[1], 0, "index"), True, 0))

            for div_soup in soup.find_all("div", class_="col-md-2"):
                url_temp = div_soup.find("a", target="_blank").get("href")
                title_text = div_soup.find("h5").get_text().strip()
                detail_url = "http://aso100.com/app/baseinfo/appid/" + url_temp.split("/")[4] + "/country/cn"
                url_list.append((detail_url, (keys[0], keys[1], int(title_text.split(".")[0]), "detail"), False, 0))

        elif keys[-1] == "detail":
            app = App(softgame="", url=url, source=keys[0]+","+",".join(keys[1]))

            app.a_name = soup.find("h3", class_="appinfo-title").get_text().strip()
            app.a_description = soup.find("div", class_="desc").get_text().strip()
            app.a_classify = ",".join(keys[1])
            app.a_subtitle = str(keys[2])
            app.a_getdate = "2000-01-01"

            app.a_picurl = soup.find("div", class_="appname clearfix").find("img").get("src").strip()

            tr_div = soup.find("table", class_="base-info base-area").find("tbody").find_all("tr")
            app.a_publisher = tr_div[0].find_all("td")[1].get_text().strip()
            app.a_updatedate = datetime.datetime.strptime(tr_div[3].find_all("td")[1].get_text().strip(), "%Y年%m月%d日")
            app.a_pkgname = tr_div[4].find_all("td")[1].get_text().strip()
            app.a_version = tr_div[5].find_all("td")[1].get_text().strip()
            app.a_bytes = spider.get_string_num(tr_div[6].find_all("td")[1].get_text(), base=1024)
            app.a_install = keys[2]

            save_list.append(app)

        return 1, url_list, save_list
