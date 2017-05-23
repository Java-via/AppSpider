# _*_ coding: utf-8 _*_

import logging
import spider

DB_HOST = "localhost"
DB_USER = "mysql_apps"
DB_PWD = "mysql_apps123"
DB_DB = "data_apps"
DB_CHARSET = "utf8"

# ---for test in local---
# DB_HOST = "127.0.0.1"
# DB_USER = "root"
# DB_PWD = "123"
# DB_DB = "app_db"
# DB_CHARSET = "utf8"

DB_SQL_BASIC = "insert into t_apps_basic (a_pkgname, a_name, a_url, a_picurl, " \
               "a_publisher, a_subtitle, a_description, a_classify, a_defaulttags, " \
               "a_softgame, a_source, a_getdate) " \
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

DB_SQL_BASIC_UP = "update t_apps_basic set a_name=%s, a_url=%s, a_picurl=%s, "\
                  "a_publisher=%s, a_subtitle=%s, a_description=%s, a_classify=%s, a_defaulttags=%s, " \
                  "a_softgame=%s, a_getdate=%s where a_source=%s and a_pkgname = %s;"

DB_SQL_ADD = "insert into t_apps_additional (a_pkgname, a_name, a_url, a_picurl, " \
             "a_bytes, a_updatedate, a_version, a_install, a_like, a_comment, a_score, " \
             "a_softgame, a_source, a_getdate)" \
             "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


class UpdateSaver(spider.SaverMysql):
    """
    for basic if same then update else then insert end
    """

    def __init__(self, source, is_update=True):
        """
        constructor
        """
        spider.SaverMysql.__init__(self, host=DB_HOST, user=DB_USER, passwd=DB_PWD, database=DB_DB, charset=DB_CHARSET)
        self.source = source
        self.is_update = is_update

        self.cursor.execute("select a_pkgname from t_apps_basic where a_source = %s;", self.source)
        self.pkgset = set([item[0] for item in self.cursor.fetchall()])
        return

    def item_save(self, url, keys, item):
        """
        item save
        """
        # add basic
        if self.is_update and (item.a_pkgname in self.pkgset):
            logging.debug("Saver update_basic %s", item.a_pkgname)
            self.cursor.execute(DB_SQL_BASIC_UP, item.get_update_items())
        else:
            logging.debug("Saver insert_basic %s", item.a_pkgname)
            self.cursor.execute(DB_SQL_BASIC, item.get_base_items())
        self.pkgset.add(item.a_pkgname)

        # add additional
        logging.debug("Saver insert_additional %s", item.a_pkgname)
        self.cursor.execute(DB_SQL_ADD, item.get_additional_items())
        return True
