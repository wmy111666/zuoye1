# -*- coding: utf-8 -*-
"""
reader_manager.py
读者管理模块：读者信息管理、学院统计、等级分布。
"""
from mongodb_connect import get_db


def add_reader(reader):
    """新增一位读者"""
    return get_db().readers.insert_one(reader).inserted_id


def find_all():
    """返回全部读者"""
    return list(get_db().readers.find())


def find_by_card(card_no):
    """按借阅证号查找读者"""
    return get_db().readers.find_one({'card_no': card_no})


def update_reader(card_no, updates):
    """更新读者信息，updates 为要修改的字段字典"""
    db = get_db()
    result = db.readers.update_one({'card_no': card_no}, {'$set': updates})
    return result.modified_count


def delete_reader(card_no):
    """删除一位读者"""
    return get_db().readers.delete_one({'card_no': card_no}).deleted_count


def count_readers():
    """读者总数"""
    return get_db().readers.count_documents({})


def college_stats():
    """按学院统计读者数量"""
    pipeline = [
        {'$group': {'_id': '$college', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    return list(get_db().readers.aggregate(pipeline))


def level_stats():
    """按借阅等级统计分布"""
    pipeline = [
        {'$group': {'_id': '$level', 'count': {'$sum': 1}}}
    ]
    return list(get_db().readers.aggregate(pipeline))


def distinct_colleges():
    """获取全部学院清单"""
    return get_db().readers.distinct('college')
