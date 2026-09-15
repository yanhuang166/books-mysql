# 爬虫---》数据库

import pymysql
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time



# ① 连数据库（注意：写在循环外面！）
conn = pymysql.connect(
    host='localhost',
    user='root',
    password=input('输入密码'),
    database='books',
    charset='utf8mb4'
)
cursor = conn.cursor()

url = 'https://books.toscrape.com/'
page_url = url
count = 0

while page_url and count < 1000:
    page_response = requests.get(page_url, timeout=10)
    page_response.raise_for_status()
    page_response.encoding = page_response.apparent_encoding
    soup = BeautifulSoup(page_response.text, 'html.parser')

    for one_book in soup.find_all('article', class_='product_pod'):
        one_book_id = urljoin(page_url, one_book.find('h3').find('a')['href'])
        try:
            response = requests.get(one_book_id, timeout=10)
            response.encoding = response.apparent_encoding
            detail = BeautifulSoup(response.text, 'html.parser')
            name = detail.find('h1').text
            price = detail.find('p', class_='price_color').text.replace('£', '')
            stock = detail.find('p', class_='instock availability').text.strip()
            star = detail.find('p', class_='star-rating')['class'][1]

        # ①：简介（防御式写法，你写过）+ 直接入库（不再 append 到列表）
        # SQL: INSERT INTO book_spider (书名, 价格, 库存, 星标数, 简介) VALUES (%s, %s, %s, %s, %s)

            desc = '无简介'
            desc_div = detail.find('div', id='product_description')
            if desc_div:
                desc_p = desc_div.find_next_sibling('p')
                if desc_p:
                    desc = desc_p.text
            # IGNORE 的意思：撞上唯一键（重复）就跳过，不报错
            cursor.execute('insert ignore into book_spider(详情页URL,书名,价格,库存,星标数,简介) values (%s,%s,%s,%s,%s,%s)',
                       (one_book_id,name, price, stock, star, desc))

        except Exception as e:
            print(f'第{count+1}本丢失 跳过{e}')
            continue
        count += 1
        if count % 50 == 0:  # 每 50 条提交一次
            conn.commit()
        print(f'已入库 {count} 本')
        time.sleep(0.5)

    next_li = soup.find('li', class_='next')
    page_url = urljoin(page_url, next_li.find('a')['href']) if next_li else None

# TODO ②：提交并关闭连接
conn.commit()
cursor.close()
conn.close()