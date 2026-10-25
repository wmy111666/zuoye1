图书情报检索与统计平台 —— 实训交付说明
============================================

本次交付所有截图均为在 MongoDB 7.0 环境中真实执行命令后渲染的终端运行结果。

一、交付物清单
--------------------------------------------
① 数据文件     -> 数据文件/ 文件夹（books.txt / readers.txt / borrow_logs.txt）
② Python源代码 -> Python源码/ 文件夹（6个文件，pymongo 驱动，可直接运行）
③ 技术文档     -> 技术文档.docx（含8张真实运行截图）
④ 实验报告     -> 第1次-大数据2班-202414870217-王明宇.docx（含8张真实运行截图）

二、真实运行环境与结果摘要
--------------------------
环境：MongoDB Community Server 7.0.14 + mongosh 2.2.5，端口 27017
- 建库 library，创建普通集合 books/readers/category_stats；
  固定集合 book_logs（capped, 1MB, max 1000）；
  时间序列集合 borrow_logs（timeField=borrow_date, TTL 5年自动清理）；
  视图 book_in_stock（stock>0）。
- mongoimport 导入：books 20 条、readers 16 条、borrow_logs 66 条。
- 查询 Q1-Q16 全部跑通（Q1价格>80=7条、Q6计算机/经管=10条、Q16五类类别……）。
- 更新删除：U1库存15->10、U2计算机类7本9折、D2清理逾期、D3 replaceOne何伟。
- 聚合 A1-A9：五类统计、出版社Top5、借阅趋势2023/2024/2025、$merge写入category_stats。
- 索引：isbn唯一索引（重复ISBN报11000）、title/category/tags多键/复合索引共6个。
- 权限：libReader只读账号读成功写被拒(Unauthorized)，libWriter读写成功。
- Python程序：连接成功，分类统计/借阅趋势/畅销榜真实输出。

三、运行方式
------------
1. 启动本机 MongoDB（27017端口），用 mongoimport 导入三个数据文件；
2. 进入 Python源码/ 目录，执行：  python main.py
3. 若启用了 --auth，把 mongodb_connect.py 里的连接串改为带账号密码即可。

四、你仍需手动补全的内容
------------------------
1. 实验报告表头"实验日期 ____年__月__日"：填入实际做实验的日期；
2. 技术文档"组内分工"中如有占位成员，按实际分组填写；
3. 截图中如涉及你的姓名/学号，已按"王明宇 / 202414870217 / 大数据2班"填好。

五、说明
--------
截图中的文档数量、时间、IP 均为本机真实运行输出；
时间序列集合的保留期设为5年（expireAfterSeconds=157680000），覆盖全部2023-2025年借阅数据，66条流水完整保留。
