# _*_ coding: utf-8 _*_

"""
app_parser by zhangjie
"""

import spider


class Parser(spider.Parser):
    """
    class of Parser
    """

    def htm_parse(self, priority, url, keys, deep, critical, repeat, content):
        """
        html parser
        """
        return content
