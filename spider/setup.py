# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from distutils.core import setup

setup(
    name="spider",
    version="3.0.0",
    author="xianhu",
    author_email="qixianhu@qq.com",
    keywords=[
        "spider",
        "crawler",
        "web spider",
        "web crawler",
        "thread spider",
        "thread crawler",
        "multiprocess spider",
        "multiprocess crawler",
    ],
    packages=[
        "spider",
        "spider.instances",
        "spider.threads",
        "spider.utilities",
    ],
    package_data={
        "": ["*.conf"],             # all *.conf in all package
    },
    install_requires=[
        "bs4 >= 4.4.0",             # beautifulsoup4
        "chardet >= 2.3.0",         # chardet
        "PyMySQL >= 0.7.2",         # PyMySQL
        "pybloom >= 2.0.0",         # pybloom, from github
    ]
)
