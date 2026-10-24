# -*- coding: utf-8 -*-
"""
borrow_manager.py
借阅管理模块：借阅登记、归还处理、逾期查询。
"""
from datetime import datetime
from mongodb_connect import get_db


def borrow_book(reader_card, book_isbn, borrow_date=None):
    """借阅登记，插入一条借出记录"""
    if borrow_date is None:
        borrow_date = datetime.now()
    doc = {
        'borrow_date': borrow_date,
        'reader_card': reader_card,
        'book_isbn': book_isbn,
        'status': '借出'
    }
    return get_db().borrow_logs.insert_one(doc).inserted_id


def return_book(reader_card, book_isbn, return_date=None):
    """归还处理，将对应的借出记录更新为已归还"""
    if return_date is None:
        return_date = datetime.now()
    db = get_db()
    result = db.borrow_logs.update_many(
        {'reader_card': reader_card, 'book_isbn': book_isbn, 'status': '借出'},
        {'$set': {'status': '已归还', 'return_date': return_date}}
    )
    return result.modified_count


def query_overdue():
    """查询逾期记录"""
    return list(get_db().borrow_logs.find({'status': '逾期'}))


def query_borrowed():
    """查询当前借出记录"""
    return list(get_db().borrow_logs.find({'status': '借出'}))


def query_by_reader(reader_card):
    """查询某读者的全部借阅记录"""
    return list(get_db().borrow_logs.find({'reader_card': reader_card}))


def count_borrows():
    """借阅记录总数"""
    return get_db().borrow_logs.count_documents({})
