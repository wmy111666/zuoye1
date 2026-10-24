# -*- coding: utf-8 -*-
"""
stat_manager.py
统计分析模块：分类统计、借阅趋势、畅销榜（使用聚合管道）。
"""
from mongodb_connect import get_db


def category_stats():
    """分类统计：按类别分组，统计库存总量、平均价格、图书数量，按库存总量降序"""
    pipeline = [
        {'$group': {
            '_id': '$category',
            'total_stock': {'$sum': '$stock'},
            'avg_price': {'$avg': '$price'},
            'book_count': {'$sum': 1}
        }},
        {'$sort': {'total_stock': -1}}
    ]
    return list(get_db().books.aggregate(pipeline))


def borrow_trend():
    """借阅趋势：按年份分组统计借阅量，格式化输出为 '2024年'"""
    pipeline = [
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y年', 'date': '$borrow_date'}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]
    return list(get_db().borrow_logs.aggregate(pipeline))


def hot_books(limit=5):
    """畅销榜：按借阅次数降序取前 limit 本"""
    return list(get_db().books.find().sort('borrow_count', -1).limit(limit))


def publisher_top(n=5):
    """出版社图书数量排行，取前 n 家"""
    pipeline = [
        {'$group': {'_id': '$publisher', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': n}
    ]
    return list(get_db().books.aggregate(pipeline))


def category_sales():
    """按类别统计销售额（单价 × 借阅次数），保留两位小数"""
    pipeline = [
        {'$project': {
            'category': 1,
            'sales': {'$round': [{'$multiply': ['$price', '$borrow_count']}, 2]}
        }},
        {'$group': {'_id': '$category', 'total_sales': {'$sum': '$sales'}}},
        {'$sort': {'total_sales': -1}}
    ]
    return list(get_db().books.aggregate(pipeline))


def top_books_by_rating(n=3):
    """评分最高的 n 本图书，显示书名与借阅次数"""
    pipeline = [
        {'$sort': {'rating': -1}},
        {'$limit': n},
        {'$project': {'_id': 0, 'title': 1, 'borrow_count': 1, 'rating': 1}}
    ]
    return list(get_db().books.aggregate(pipeline))
