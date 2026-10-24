# -*- coding: utf-8 -*-
"""
main.py
主程序：菜单式交互，串联各功能模块。
"""
from mongodb_connect import get_db, close_connection, get_stats
import book_manager, reader_manager, borrow_manager, stat_manager


def print_menu():
    print()
    print('=' * 46)
    print('       图书情报检索与统计平台')
    print('=' * 46)
    print('  1. 新增图书')
    print('  2. 查询图书（按条件）')
    print('  3. 图书评分排行')
    print('  4. 新增读者')
    print('  5. 学院统计')
    print('  6. 读者等级分布')
    print('  7. 借阅登记')
    print('  8. 归还处理')
    print('  9. 查询逾期记录')
    print(' 10. 分类统计（聚合）')
    print(' 11. 借阅趋势（按年）')
    print(' 12. 畅销图书榜')
    print(' 13. 借阅次数前5读者')
    print('  0. 退出')
    print('=' * 46)


def handle_add_book():
    book = {}
    book['isbn'] = input('请输入 ISBN：').strip()
    book['title'] = input('请输入书名：').strip()
    book['author'] = input('请输入作者：').strip()
    book['publisher'] = input('请输入出版社：').strip()
    book['category'] = input('请输入类别：').strip()
    try:
        book['price'] = float(input('请输入价格：').strip())
        book['stock'] = int(input('请输入库存：').strip())
        book['rating'] = float(input('请输入评分(0-5)：').strip())
    except ValueError:
        print('价格/库存/评分格式错误，请重新输入。')
        return
    book['tags'] = input('请输入标签（逗号分隔）：').strip().split(',')
    book['borrow_count'] = 0
    new_id = book_manager.add_book(book)
    print(f'新增成功，文档 _id = {new_id}')


def handle_query_book():
    print('查询方式：1=全部  2=按ISBN  3=按价格  4=按类别  5=按书名')
    mode = input('请选择：').strip()
    if mode == '1':
        result = book_manager.find_all()
    elif mode == '2':
        isbn = input('请输入ISBN：').strip()
        result = book_manager.find_by_isbn(isbn)
        if result:
            print(result)
        else:
            print('未找到该图书。')
            return
    elif mode == '3':
        gt = input('价格大于(直接回车跳过)：').strip()
        lt = input('价格小于(直接回车跳过)：').strip()
        result = book_manager.find_by_price(
            gt=float(gt) if gt else None,
            lt=float(lt) if lt else None
        )
    elif mode == '4':
        cat = input('请输入类别：').strip()
        result = book_manager.find_by_category(cat)
    elif mode == '5':
        kw = input('请输入书名关键字：').strip()
        result = book_manager.search_title(kw)
    else:
        print('无效选项。')
        return
    print(f'共查到 {len(result)} 条：')
    for b in result:
        print(b.get('title'), b.get('price'), b.get('rating'), b.get('category'))


def handle_rating_rank():
    n = input('请输入排行条数(默认5)：').strip() or '5'
    result = book_manager.rating_rank(int(n))
    print(f'评分排行前 {len(result)} 本：')
    for i, b in enumerate(result, 1):
        print(f'{i}. {b.get("title")}  评分 {b.get("rating")}')


def handle_add_reader():
    reader = {}
    reader['card_no'] = input('请输入借阅证号：').strip()
    reader['name'] = input('请输入姓名：').strip()
    reader['college'] = input('请输入学院：').strip()
    reader['email'] = input('请输入邮箱(可空)：').strip() or None
    reader['phone'] = input('请输入电话：').strip()
    reader['level'] = input('请输入等级(普通/高级/教师)：').strip()
    reader['fav_categories'] = input('请输入偏好类别（逗号分隔）：').strip().split(',')
    new_id = reader_manager.add_reader(reader)
    print(f'新增读者成功，_id = {new_id}')


def handle_college_stats():
    result = reader_manager.college_stats()
    print('各学院读者数量：')
    for r in result:
        print(f'{r["_id"]}：{r["count"]} 人')


def handle_level_stats():
    result = reader_manager.level_stats()
    print('读者等级分布：')
    for r in result:
        print(f'{r["_id"]}：{r["count"]} 人')


def handle_borrow():
    card = input('请输入读者证号：').strip()
    isbn = input('请输入图书ISBN：').strip()
    new_id = borrow_manager.borrow_book(card, isbn)
    print(f'借阅登记成功，记录 _id = {new_id}')


def handle_return():
    card = input('请输入读者证号：').strip()
    isbn = input('请输入图书ISBN：').strip()
    n = borrow_manager.return_book(card, isbn)
    print(f'已处理 {n} 条归还记录。')


def handle_overdue():
    result = borrow_manager.query_overdue()
    print(f'共有 {len(result)} 条逾期记录：')
    for r in result:
        print(r.get('borrow_date'), r.get('reader_card'), r.get('book_isbn'))


def handle_category_stats():
    result = stat_manager.category_stats()
    print('分类统计（库存总量/平均价格/图书数量）：')
    for r in result:
        print(f'{r["_id"]}：库存 {r["total_stock"]}，均 {r["avg_price"]:.2f} 元，{r["book_count"]} 本')


def handle_borrow_trend():
    result = stat_manager.borrow_trend()
    print('借阅趋势（按年）：')
    for r in result:
        print(f'{r["_id"]}：{r["count"]} 次')


def handle_hot_books():
    n = input('请输入榜单条数(默认5)：').strip() or '5'
    result = stat_manager.hot_books(int(n))
    print(f'畅销图书前 {len(result)} 本：')
    for i, b in enumerate(result, 1):
        print(f'{i}. {b.get("title")}  借阅 {b.get("borrow_count")} 次')


def handle_top_readers():
    pipeline = [
        {'$group': {'_id': '$reader_card', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ]
    result = list(get_db().borrow_logs.aggregate(pipeline))
    print('借阅次数前5读者：')
    for r in result:
        print(f'{r["_id"]}：{r["count"]} 次')


def main():
    # 启动时打印数据库连接状态与各集合文档总数
    try:
        stats = get_stats()
        print('数据库连接成功：MongoDB @ 127.0.0.1:27017 / library')
        print(f'集合文档数：books={stats["books"]}，readers={stats["readers"]}，borrow_logs={stats["borrow_logs"]}')
    except Exception as e:
        print('数据库连接失败，请确认 MongoDB 服务已启动。')
        print('错误信息：', e)
        return

    handlers = {
        '1': handle_add_book,
        '2': handle_query_book,
        '3': handle_rating_rank,
        '4': handle_add_reader,
        '5': handle_college_stats,
        '6': handle_level_stats,
        '7': handle_borrow,
        '8': handle_return,
        '9': handle_overdue,
        '10': handle_category_stats,
        '11': handle_borrow_trend,
        '12': handle_hot_books,
        '13': handle_top_readers,
    }

    while True:
        print_menu()
        choice = input('请选择功能(0-13)：').strip()
        if choice == '0':
            print('正在关闭数据库连接，感谢使用！')
            close_connection()
            break
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print('无效选项，请重新输入。')


if __name__ == '__main__':
    main()
