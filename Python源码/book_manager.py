# -*- coding: utf-8 -*-
"""
book_manager.py
图书管理模块：图书增删改查、条件检索、评分排行。
"""
from mongodb_connect import get_db


def add_book(book):
    """新增一本图书，book 为字典"""
    db = get_db()
    result = db.books.insert_one(book)
    return result.inserted_id


def add_books(book_list):
    """批量新增图书"""
    db = get_db()
    return db.books.insert_many(book_list).inserted_ids


def find_all():
    """返回全部图书"""
    return list(get_db().books.find())


def find_by_isbn(isbn):
    """按 ISBN 精确查找"""
    return get_db().books.find_one({'isbn': isbn})


def find_by_price(gt=None, lt=None):
    """按价格范围查找，gt=大于，lt=小于"""
    query = {}
    price = {}
    if gt is not None:
        price['$gt'] = gt
    if lt is not None:
        price['$lt'] = lt
    if price:
        query['price'] = price
    return list(get_db().books.find(query))


def find_by_category(category):
    """按类别查找"""
    return list(get_db().books.find({'category': category}))


def search_title(keyword):
    """按书名模糊匹配"""
    from bson.regex import Regex
    return list(get_db().books.find({'title': Regex(keyword)}))


def update_stock(isbn, inc):
    """更新图书库存，inc 为增减量（可正可负）"""
    db = get_db()
    result = db.books.update_one({'isbn': isbn}, {'$inc': {'stock': inc}})
    return result.modified_count


def update_price(category, factor):
    """将某类别图书价格乘以 factor（如0.9 表示打9折）"""
    db = get_db()
    result = db.books.update_many({'category': category}, {'$mul': {'price': factor}})
    return result.modified_count


def delete_by_isbn(isbn):
    """按 ISBN 删除一本图书"""
    db = get_db()
    return db.books.delete_one({'isbn': isbn}).deleted_count


def delete_by_category(category):
    """按类别删除图书"""
    db = get_db()
    return db.books.delete_many({'category': category}).deleted_count


def rating_rank(limit=5):
    """按评分降序取前 limit 本"""
    return list(get_db().books.find().sort('rating', -1).limit(limit))
