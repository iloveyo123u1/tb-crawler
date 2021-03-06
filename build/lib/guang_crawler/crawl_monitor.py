#! /usr/bin/env python
# coding: utf-8

"""
    调用淘宝api抓商品，上下架，打term，抓主图
    shop.crawl_status 0=完成  1=等待  2=正在爬
    item.crawl_status 0=等待  1=完成html  2=完成图片
"""
import gflags
import logging
import time
import traceback
import os

from pygaga.helpers.logger import log_init
from pygaga.helpers.dbutils import get_db_engine
from guang_crawler.taobao_api import get_taobao_items, get_top
from taobao_item import TaobaoItem
from taobao_category import TaobaoCategory
from taobao_term import TermFactory

logger = logging.getLogger('CrawlLogger')
FLAGS = gflags.FLAGS
gflags.DEFINE_boolean('all', False, "update all shop")
gflags.DEFINE_integer('shopid', 0, "update shop id")
gflags.DEFINE_boolean('force', False, "is update offline shops?")
gflags.DEFINE_boolean('commit', False, "is commit data into database?")
gflags.DEFINE_boolean('debug_parser', False, 'is debug?')
gflags.DEFINE_string('path', "/space/wwwroot/image.guang.j.cn/ROOT/images/", "is upload to nfs?")

SHOP_CRAWL_STATUS_NONE = 0
SHOP_CRAWL_STATUS_WAIT = 1
SHOP_CRAWL_STATUS_CRAWLING = 2
SHOP_CRAWL_STATUS_ERROR = 3

ITEM_STATUS_BLACKLIST = 3


def crawl_all_shop():
    if FLAGS.force:
        return crawl_shop("select id, type, url, term_limits from shop where crawl_status=1 and type<=2")
    else:
        return crawl_shop("select id, type, url, term_limits from shop where crawl_status=1 and status=1 and type<=2")


def crawl_one_shop(shopid):
    return crawl_shop("select id, type, url, term_limits from shop where id=%s" % shopid)

def imgExists(shop_id, local_pic_url):
    big_path = "%s/%s/big/%s" % (FLAGS.path, shop_id, local_pic_url)
    mid2_path = "%s/%s/mid2/%s" % (FLAGS.path, shop_id, local_pic_url)
    mid_path = "%s/%s/mid/%s" % (FLAGS.path, shop_id, local_pic_url)
    return os.path.isfile(big_path) and os.path.isfile(mid2_path) and os.path.isfile(mid_path)

def doCrawl(shop_id, numids_set):
    """
        注意：
            下面这3行完全是为了满足get_taobao_items的第二个参数限制，组装成类似数据库查询结果，没啥意义
    """
    num_iids = []
    for id in numids_set:
        num_iids.append((shop_id, id))

    return_item_list = []
    results = get_taobao_items(get_top(), num_iids, fn_join_iids=lambda x: ','.join([str(i[1]) for i in x]))
    for r in results:
        for iid, item in r.items.iteritems():
            if item['resp']:
                return_item_list.append(dict(item['resp']))
    return return_item_list

def filterNumIds(db, shop_id, tb_numids_set):
    allNumIds = db.execute("SELECT num_id FROM item WHERE shop_id = %s AND status = 1" % shop_id)
    db_numids = []
    for numids in allNumIds:
        db_numids.extend(numids[0].split(','))
    db_numids_set = set(db_numids)

    #返回tb中有但是db中没有的元素，这就是要新增的, 也可能是重新上线的
    new_numids_set = tb_numids_set - db_numids_set
    #返回db中有但是tb中没有的元素，这就是要offline的
    offShelf_numids_set = db_numids_set - tb_numids_set
    #返回tb和db的公共元素，检查是否需要更新价格和主图
    common_numids_set = tb_numids_set & db_numids_set

    return new_numids_set, offShelf_numids_set, common_numids_set

def crawl_shop(sql):
    db = get_db_engine()
    shops = db.execute(sql)

    # debug
    if FLAGS.debug_parser:
        import pdb
        pdb.set_trace()

    # global, all shop use
    tb_category = TaobaoCategory()
    term_factory = TermFactory()

    for shop in shops:
        shop_id = shop[0]
        shop_type = shop[1]
        shop_url = shop[2]
        shop_termLimits = shop[3]

        defaultCampaign = list(db.execute(
            "select id, default_uctrac_price from campaign where shop_id=%s and system_status = 1 and delete_flag = 0" % shop_id))
        if not defaultCampaign:
            logger.error("can not get the default campaign for shop: %s", shop_id)
            continue

        #1.更新shop crawl_status=2
        #2.crawl
        #3.更新shop crawl_status=0
        #db.execute("update shop set crawl_status=%s where id=%s", SHOP_CRAWL_STATUS_CRAWLING, shop_id)

        # 店铺的所有商品num id
        allTbNumIds = db.execute("SELECT itemids FROM tb_shop_item WHERE shopid = %s", shop_id)
        tb_numids = []
        for ids in allTbNumIds:
            tb_numids.extend(ids[0].split(','))
        tb_numids_set = set(tb_numids)

        # 过滤
        new_numids_set, offShelf_numids_set, common_numids_set = filterNumIds(db, shop_id, tb_numids_set)

        if len(new_numids_set) == 0:
            logger.info("crawling shop: %s %s", shop_id, shop_url)

            new_item_list = doCrawl(shop_id, new_numids_set)
            if new_item_list:
                new_num = 0
                new_numiid = []
                update_num = 0
                update_numiid = []
                for dict_item in new_item_list:
                    num_id = str(dict_item['num_iid'])
                    n_cid = dict_item['cid']
                    tb_title = dict_item['title']
                    tb_detail_url = str(dict_item['detail_url'])
                    tb_price = float(dict_item['price'])
                    tb_pic_url = str(dict_item['pic_url'])

                    volume = 0
                    if dict_item.has_key('volume'):
                        volume = dict_item['volume']

                    #检查该商品是否重新上架
                    db_item = list(db.execute(
                        "select id, title, pic_url, local_pic_url, price, manual_set, status from item where shop_id=%s and num_id=%s" % (
                        shop_id, str(num_id))))
                    if db_item:
                        db_status = db_item[0][6]
                        db_manual_set = db_item[0][5]
                        db_price = db_item[0][4]
                        db_local_pic_url = db_item[0][3]
                        db_pic_url = db_item[0][2]
                        db_title = db_item[0][1]
                        db_item_id = db_item[0][0]

                        #update
                        if db_status == ITEM_STATUS_BLACKLIST:
                            continue
                        if db_manual_set == 1:
                            # 人工设置了图片和title
                            if not imgExists(shop_id, db_local_pic_url):
                                # 老图片不存在，需要重新下载
                                tb_item = TaobaoItem(shop_id, db_item_id, num_id)
                                tb_item.setPicUrl(tb_pic_url, db_pic_url)
                                if tb_price != db_price:
                                    tb_item.price = tb_price

                                # TODO db update

                        else:
                            tb_item = TaobaoItem(shop_id, db_item_id, num_id, dict_item['title'],
                                                 dict_item['detail_url'],
                                                 dict_item['price'], dict_item['pic_url'], volume)
                            tb_item.setPicUrl(dict_item['pic_url'], db_pic_url)

                            update_numiid.append(num_id)

                            # TODO db update
                        update_num += 1
                    else:
                        #add
                        tb_item = TaobaoItem(shop_id, 0, num_id, tb_title, tb_detail_url,
                                             tb_price, dict_item['pic_url'], volume)
                        tb_item.category = tb_category.getCategoryPath(n_cid)
                        tb_item.termIds = tb_item.matchTaobaoTerms(term_factory, str(shop_termLimits))
                        tb_item.setPicUrl(dict_item['pic_url'], "")
                        tb_item.setCampaign(defaultCampaign)

                        new_numiid.append(num_id)

                        # TODO db add

                        new_num += 1

                logger.info("shop %s new item num=%s,update item num=%s", shop_id, new_num, update_num)

        if offShelf_numids_set:
            #offline
            #db.execute("update item set status=2 where num_id in (%s)", ', '.join(offShelf_numids_set))
            logger.info("shop %s off shelf item num=%s", shop_id, len(offShelf_numids_set))

        if common_numids_set:
            #validate price pic_url
            common_item_list = doCrawl(shop_id, common_numids_set)
            if common_item_list:
                for dict_item in common_item_list:
                    num_id = str(dict_item['num_iid'])
                    title = dict_item['title']
                    price = float(dict_item['price'])
                    pic_url = str(dict_item['pic_url'])
                    db_item = list(db.execute(
                        "select id, title, pic_url, local_pic_url, price, manual_set, status from item where shop_id=%s and num_id=%s" % (
                        shop_id, num_id)))
                    if db_item:
                        if db_item[0][6] == ITEM_STATUS_BLACKLIST:
                            continue
                        else:
                            id = int(db_item[0][0])

                            tb_item = TaobaoItem(shop_id, id, num_id)
                            if dict_item.has_key('volume'):
                                tb_item.volume = int(dict_item['volume'])
                            if price != db_item[0][4]:
                                tb_item.price = price
                            if title != db_item[0][1]:
                                tb_item.title = title
                            if pic_url != db_item[0][2]:
                                tb_item.setPicUrl(pic_url, db_item[0][2])

                        # TODO db update

            logger.info("shop %s common item num=%s ", shop_id, len(common_numids_set))

            #db.execute("update shop set crawl_status=%s where id=%s", SHOP_CRAWL_STATUS_NONE, shop_id)

if __name__ == "__main__":
    log_init("CrawlLogger", "sqlalchemy.*")
    if FLAGS.all:
        crawl_all_shop()
    elif FLAGS.shopid > 0:
        crawl_one_shop(FLAGS.shopid)
