# _*_ coding: utf-8 _*_

"""
config file
"""

import datetime


class App(object):
    """
    class of App
    """

    def __init__(self, softgame, url, source):
        """
        constructor
        """
        # public data
        self.a_pkgname = ""
        self.a_name = ""
        self.a_url = url
        self.a_picurl = ""

        self.a_softgame = softgame
        self.a_source = source
        self.a_getdate = datetime.date.today()

        # base data
        self.a_publisher = ""
        self.a_subtitle = ""
        self.a_description = ""

        self.a_classify = ""        # A:A1,D:D1,E
        self.a_defaulttags = ""     # A,B,D

        # additional data
        self.a_bytes = 0
        self.a_updatedate = None
        self.a_version = ""

        self.a_install = 0
        self.a_like = 0
        self.a_comment = 0
        self.a_score = 0.0
        return

    def get_base_items(self):
        """
        get base item list
        """
        return [
            self.a_pkgname, self.a_name, self.a_url, self.a_picurl,
            self.a_publisher, self.a_subtitle, self.a_description, self.a_classify, self.a_defaulttags,
            self.a_softgame, self.a_source, self.a_getdate
        ]

    def get_additional_items(self):
        """
        get additional item list
        """
        return [
            self.a_pkgname, self.a_name, self.a_url, self.a_picurl,
            self.a_bytes, self.a_updatedate, self.a_version, self.a_install, self.a_like, self.a_comment, self.a_score,
            self.a_softgame, self.a_source, self.a_getdate
        ]

    def get_update_items(self):
        """
        get base item list(update)
        """
        return [
            self.a_name, self.a_url, self.a_picurl,
            self.a_publisher, self.a_subtitle, self.a_description, self.a_classify, self.a_defaulttags,
            self.a_softgame, self.a_getdate,
            self.a_source, self.a_pkgname
        ]
