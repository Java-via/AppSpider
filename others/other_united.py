# _*_ coding: utf-8 _*_

"""
other_united by xianhu
"""

import re
import logging
import pymysql
import Levenshtein

DB_HOST = "localhost"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"
logging.basicConfig(level=logging.DEBUG)

SQL_INSERT = "INSERT INTO t_apps_basic_united (" \
             "a_pkgname, a_pkgname_list, " \
             "a_name, a_name_list, " \
             "a_url, a_url_list, " \
             "a_picurl, a_picurl_list, " \
             "a_publisher, a_publisher_list, " \
             "a_description, a_description_list, " \
             "a_classify, a_defaulttags, " \
             "a_softgame, a_softgame_list, " \
             "a_source_list, a_getdate) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

SQL_IOS = """
"""


def samiliar(string1, string2):
    """
    compare two strings
    """
    return Levenshtein.ratio(get_string_strip(string1), get_string_strip(string2))


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""


def basic_catchapps():
    """
    unit data
    """
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    cur.execute("SELECT * FROM t_apps_basic_new WHERE a_source NOT LIKE '%iphone%' ORDER BY a_pkgname;")

    current_app = []
    for app_info in cur.fetchall():
        a_id, a_pkgname, a_name, a_url, a_picurl, a_pub, a_sub, a_des, a_classify, a_tags, a_softname, a_source, a_date = \
            [get_string_strip(str(item)) for item in app_info]

        if current_app and ((a_pkgname == current_app[0]) or (a_pkgname in current_app[1]) or (
                (samiliar(a_pkgname, current_app[0]) >= 0.7) and
                (
                    (samiliar(a_name, current_app[2]) >= 0.9) or
                    (samiliar(a_des, current_app[10]) >= 0.7)
                ))):
            current_app[1].add(a_pkgname)
            current_app[3].add(a_name)
            current_app[5].add(a_url)
            current_app[7].add(a_picurl)
            current_app[9].add(a_pub)
            current_app[11].add(a_des)
            current_app[12].update(a_classify.split())
            current_app[13].update(a_tags.split())
            current_app[15].add(a_softname)
            current_app[16].add(a_source)
        else:
            if current_app:
                logging.debug("insert: %s, %s", current_app[0], current_app[2])
                cur.execute(SQL_INSERT, [i if isinstance(i, str) else "\n".join(i) for i in current_app])
            current_app = [
                a_pkgname, set(iter([a_pkgname])),
                a_name, set(iter([a_name])),
                a_url, set(iter([a_url])),
                a_picurl, set(iter([a_picurl])),
                a_pub, set(iter([a_pub])),
                a_des, set(iter([a_des])),
                set(iter([a_classify])), set(iter([a_tags])),
                a_softname, set(iter([a_softname])),
                set(iter([a_source])), "2016-09-10"
            ]
    return

if __name__ == '__main__':
    basic_catchapps()
