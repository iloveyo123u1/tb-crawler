#!/usr/bin/env python

import glob
from distutils.core import setup
from guang_crawler import __version__ as version
from setuptools import find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

#PRE REQUIRED
# sudo apt-get install -y --force-yes libxml2-dev libxslt1-dev libjpeg-dev libpng-dev python-mysqldb
# sudo easy_install dateutils requests urllib3

setup(
    name = 'guang_crawler',
    version = version,
    description = 'adgaga common python libs',
    long_description = long_description,
    author = 'Chris Song',
    author_email = 'chuansheng.song@langtaojin.com',
    url = 'ssh://chuansheng.song@review2.jcndev.com:29418/taobao-crawler2',
    packages = find_packages(exclude=[]),
    exclude_package_data={'': []},
    data_files=[('qzone/templates', glob.glob('qzone/templates/*')),],
    scripts = ['guang_crawler/crawl_image.py',
               'guang_crawler/crawl_item.py',
               'guang_crawler/crawl_shop.py',
               'guang_crawler/crawl.py',
               'guang_crawler/fix_thumb.py',
               'guang_crawler/crawl_image_server.py',
               'guang_crawler/process_taobaoke.py',
               'guang_crawler/get_taobao_report.py',
               'guang_crawler/get_comments.py',
               'guang_crawler/mark_shop2crawl.py',
               'guang_crawler/quick_update_taobao_status.py',
               'guang_crawler/check_shop.py',
               'guang_crawler/update_shop_level.py',
               'guang_crawler/update_item_title_image.py',
               'guang_crawler/get_comments_total.py',
               'guang_crawler/replace_main_image.py',
               'guang_crawler/collocation_small_image.py',
               'guang_crawler/crawl_taobao.py',
               'guang_crawler/crawl_taobao_new.py',
               'guang_crawler/crawl_shop_basic_info.py',
               'guang_crawler/crawl_shop_promotion.py',
               'guang_crawler/crawl_shop_discount.py',
               'qzone/post.py',
               'qzone/qq_login_proxy.py',
               'bin/recrawl_taobao_item.sh',
               'bin/crawl_image_server.sh',
               'bin/crawl_pending.sh',
               'bin/crawl_pending_daemon.sh',
               'bin/crawl_item_html.sh',
               'bin/crawl_item_images.sh',
               'bin/kill_crawl_images.sh',
               'bin/move_images.sh',
               'bin/crawl_redial',
               'bin/redial',
               'bin/crawl_hotest.sh',
               'bin/daily_crawl_comments',
               'bin/daily_crawl_recent_comments',
               'bin/repeat_crawl_all_comments.sh',
               'bin/repeat_crawl_all_comments_1.sh',
               'bin/repeat_crawl_all_comments_2.sh',
               'bin/crawl_taobao.sh',
               'bin/crawl_taobao_shop_extend_info.sh',
               ],
    license = "langtaojin.com",
    dependency_links = [],
    install_requires = ["sqlalchemy",
                        "redis",
                        "pymongo",
                        "zc-zookeeper-static",
                        "pykeeper",
                        "daemon",
                        "python-gflags",
                        "simplejson",
                        "jinja2",
                        "lxml",
                        "PIL",
                        "web.py",
                        "BeautifulSoup",
                        "python-dateutil",
                        "urllib3",
                        "requests",
                        "pyTOP",
                        ],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: langtaojin.com',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
