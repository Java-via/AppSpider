# _*_ coding: utf-8 _*_

import pymysql
import logging
import datetime


DB_HOST = "101.200.174.172"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_DB = "data_apps"
DB_CHARSET = "utf8"


def add_exclude():
    log_file = "addexclude_%s.log" % str(datetime.date.today())
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s", filename=log_file,
                        filemode="w")

    conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    add_exclude_sql = """
        INSERT INTO t_apps_additional_new (a_pkgname, a_name, a_url, a_picurl, a_bytes, a_updatedate, a_version, a_install,
        a_like, a_comment, a_score, a_softgame, a_source, a_getdate)
        SELECT t3.a_pkgname, t3.a_name, t3.a_url, t3.a_picurl, t3.a_bytes, t3.a_updatedate, t3.a_version, t3.a_install,
        t3.a_like, t3.a_comment, t3.a_score, t3.a_softgame, t3.a_source, t3.a_getdate
        FROM(
            SELECT a_pkgname, a_name, a_url, a_picurl, a_bytes, a_updatedate, a_version, a_install,
            a_like, a_comment, a_score, a_softgame, a_source, a_getdate
            FROM t_apps_additional_new
            WHERE a_getdate BETWEEN DATE_SUB(CURDATE(), INTERVAL 2 DAY) AND DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        UNION
            SELECT a_pkgname, a_name, a_url, a_picurl, a_bytes, a_updatedate, a_version, a_install,
            a_like, a_comment, a_score, a_softgame, a_source, DATE_ADD(a_getdate, INTERVAL 1 DAY)
            FROM t_apps_additional_new WHERE DATE(a_getdate) = DATE_SUB(CURDATE(), INTERVAL 2 DAY)
        ) t3
        LEFT JOIN t_apps_additional_new t4
        ON t3.a_pkgname = t4.a_pkgname AND t3.a_source = t4.a_source AND DATE(t3.a_getdate) = DATE(t4.a_getdate)
        WHERE t4.a_pkgname IS NULL OR t4.a_source IS NULL OR t4.a_getdate IS NULL;
    """
    try:
        cur.execute(add_exclude_sql)
        conn.commit()
    except Exception as excep:
        logging.error("Add Exclude Error: %s", excep)
