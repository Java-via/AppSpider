# _*_ coding: utf-8 _*_

"""
other_spider.py by xianhu
"""

import bs4
import json
import logging
import html2text
import PIL.Image
import pytesseract
import Levenshtein
import urllib.request


def get_ocr_captcha(image_file, language="eng"):
    """
    identify captcha from a image_file, using module: ocr(tesseract)
    """
    return pytesseract.image_to_string(PIL.Image.open(image_file), lang=language)


def get_html_text(html_content, baseurl="", bodywidth=None):
    """
    get html text from html content, using module: html2text
    """
    return html2text.html2text(html_content, baseurl=baseurl, bodywidth=bodywidth)


def get_string_similarity(string1, string2):
    """
    get similarity[0, 1] between two strings, using module: Levenshtein
    """
    return Levenshtein.ratio(string1, string2)


def get_addr_ip(ip_str, source="ipip"):
    """
    get ip address from ip_str, source can be "ipip" or "taobao"
    """
    assert source in ["ipip", "taobao"], "get_addr_ip: invalid parameter"
    url = "http://freeapi.ipip.net/%s" if source == "ipip" else "http://ip.taobao.com/service/getIpInfo.php?ip=%s"
    try:
        response = urllib.request.urlopen(url % ip_str.strip())
        return json.loads(response.read().decode("utf-8"))
    except Exception as excep:
        logging.error("get_addr_ip error: %s", excep)
    return None


def get_addr_phone(phone_str):
    """
    get phone address from phone_str, len(phone_str) must be 11 or 7
    """
    assert len(phone_str.strip()) in [7, 11], "get_addr_phone: invalid parameter"
    url = "http://www.ip138.com:8080/search.asp?action=mobile&mobile=%s" % phone_str.strip()
    try:
        response = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(response.read().decode("gb2312"), "html.parser")
        table = soup.find_all("table")[1]
        item = table.find_all("td", class_="tdc2")[1]
        return item.get_text().strip()
    except Exception as excep:
        logging.error("get_addr_phone error: %s", excep)
    return None


def test_proxy(proxies):
    """
    test proxy and output proxy status, return True or False. proxies: {"http": "http://proxy.example.com:8080/"}
    """
    handler = urllib.request.ProxyHandler(proxies=proxies if proxies else {"http": "101.200.174.172:8888"})
    opener = urllib.request.build_opener(handler)
    try:
        response = opener.open("http://www.baidu.com/s?wd=ip", timeout=10)
        soup = bs4.BeautifulSoup(response.read().decode("utf-8"), "html.parser")
        item = soup.find("div", class_="c-span21 c-span-last op-ip-detail")
        if item:
            logging.debug("test_proxy succeed: %s, %s", proxies, item.get_text().strip())
            return True
        logging.debug("test_proxy failed: item is None")
    except Exception as excep:
        logging.error("test_proxy error: %s", excep)
    return False
