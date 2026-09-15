# books-mysql

Python 爬虫将 books.toscrape.com 全站 1000 本书数据直接写入 MySQL 数据库。

## 技术栈

- Python 3
- requests / BeautifulSoup（爬取解析）
- pymysql（数据库驱动）
- MySQL 8（数据存储）

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
