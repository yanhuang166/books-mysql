# books-mysql

Python 数据全链路项目：从网页爬取 → MySQL 存储 → 数据分析 → Flask 可视化展示。

## 项目文件

| 文件 | 功能 |
|------|------|
| spider_to_mysql.py | （填：单线程爬虫 + 数据入库） |
| spider_concurrent.py | （填：多线程并发版） |
| python_sql_demo.py | （填：从数据库读数据做分析） |
| sql_join_flask.py | （填：Flask 数据展示站） |

## 技术栈

Python / requests / BeautifulSoup / pymysql / pandas / matplotlib / Flask / MySQL

## 工程亮点

- **多线程并发爬取**：5 线程同时工作，1000 本书入库约 9 分钟（串行需 50 分钟）
- **去重入库**：以详情页 URL 为唯一键（UNIQUE + INSERT IGNORE），重跑安全
- **容错设计**：单本书失败自动跳过，不影响批量任务
- **多表查询**：JOIN 星级对照表，实现按星级数字排序
- **Web 展示**：4 个页面（首页/评分/库存/Top10），数据源实时查询 MySQL

## 运行说明

1. 建库建表（需要 book_spider 和 star_level 两张表）
2. 安装依赖：`pip install requests beautifulsoup4 pymysql pandas matplotlib flask`
3. 创建 `配置文件名.py`，内容：`DB_PASSWORD = '你的密码'`
4. 运行：`python sql_join_flask.py` → 访问 `127.0.0.1:5000`

## 数据来源

books.toscrape.com（教学练习站，1000 本书）

# books-mysql

Python 爬虫将 books.toscrape.com 全站 1000 本书数据直接写入 MySQL 数据库。

## 技术栈

- Python 3
- requests / BeautifulSoup（爬取解析）
- pymysql（数据库驱动）
- MySQL 8（数据存储）
- pandas (数据清洗）

## 工程特点

- **容错设计**：单本书请求失败自动跳过，不影响批量任务
- **去重入库**：以详情页 URL 作为唯一键（UNIQUE 约束 + INSERT IGNORE），
  重跑安全——已爬取的自动跳过，缺失的自动补齐
- **批量提交**：每 50 条提交一次，兼顾性能与数据安全
- **定期限速**：每本间隔 0.5 秒，礼貌爬取

## 数据表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| 详情页URL | VARCHAR(500) | 唯一键 |
| 书名 | VARCHAR(300) | |
| 价格 | FLOAT | |
| 库存 | VARCHAR(100) | |
| 星标数 | VARCHAR(20) | |
| 简介 | TEXT | |

## 运行

1. 安装依赖：`pip install -r requirements.txt`
2. 建库建表（见 create_table.sql）
3. 运行：`python spider_to_mysql.py`

## 数据来源

books.toscrape.com（教学练习站）
