# -*- coding: utf-8 -*-
"""
mongodb_connect.py
数据库连接模块：封装与 MongoDB 的连接，供其他所有模块调用。
"""
from pymongo import MongoClient

# 连接参数统一在本模块定义
HOST = '127.0.0.1'
PORT = 27017
DB_NAME = 'library'
USERNAME = 'libWriter'
PASSWORD = 'Writer@123'  # @ 在 URL 中需编码为 %40，这里用显式参数无需编码

_client = None


def get_client():
    """获取 MongoClient 实例（单例）"""
    global _client
    if _client is None:
        _client = MongoClient(
            host=HOST, port=PORT,
            username=USERNAME, password=PASSWORD,
            authSource='admin'
        )
    return _client


def get_db():
    """返回 library 数据库对象"""
    return get_client()[DB_NAME]


def close_connection():
    """关闭数据库连接"""
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_stats():
    """返回各集合的文档总数，用于主程序启动时打印状态"""
    db = get_db()
    return {
        'books': db.books.count_documents({}),
        'readers': db.readers.count_documents({}),
        'borrow_logs': db.borrow_logs.count_documents({})
    }
