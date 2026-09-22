import pymysql
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# ① 先收集所有详情页 URL（这一步还是串行翻页，但很快——50 页列表页而已）
def collect_urls():
    urls = []
    page_url = 'https://books.toscrape.com/'
    while page_url:
        soup = BeautifulSoup(requests.get(page_url, timeout=10).text, 'html.parser')
        for h3 in soup.find_all('h3'):
            urls.append(urljoin(page_url, h3.find('a')['href']))
        next_li = soup.find('li', class_='next')
        page_url = urljoin(page_url, next_li.find('a')['href']) if next_li else None
    return urls

# ② 单个爬取函数：请求详情页 → 解析 → 返回字典（不碰数据库！）
def fetch_one(book_url):
    try:
        response = requests.get(book_url, timeout=10)
        response.encoding = response.apparent_encoding
        detail = BeautifulSoup(response.text, 'html.parser')

        name = detail.find('h1').text
        price = detail.find('p', class_='price_color').text.replace('£', '')
        stock = detail.find('p', class_='instock availability').text.strip()
        star = detail.find('p', class_='star-rating')['class'][1]

        desc = '无简介'
        desc_div = detail.find('div', id='product_description')
        if desc_div:
            desc_p = desc_div.find_next_sibling('p')
            if desc_p:
                desc = desc_p.text

        return (book_url, name, price, stock, star, desc)   # 返回元组
    except Exception as e:
        print(f'失败：{book_url} — {e}')
        return None      # ← 失败返回 None

# ③ 主流程
urls = collect_urls()

print(f'共收集 {len(urls)} 个详情页 URL')

conn = pymysql.connect(host='localhost', user='root', password=input('密码：'),
                       database='books', charset='utf8mb4')
cursor = conn.cursor()

count = 0
with ThreadPoolExecutor(max_workers=5) as executor:# 应该是设置多线程
    # TODO ①：并发爬取 → 主线程逐个入库
    # 提示：for result in executor.map(fetch_one, urls):
    #         result 是 fetch_one 的返回值（元组或 None）
    #         if result:  → cursor.execute(INSERT IGNORE ...) → count += 1
    #         每 50 条 commit
    for result in executor.map(fetch_one, urls):# result应该的一个元组，重点讲清map方法的逻辑这一行
        if result:
            cursor.execute(
                'insert ignore into book_spider(详情页URL,书名,价格,库存,星标数,简介) values (%s,%s,%s,%s,%s,%s)',
                result) # 这一行也是重点先把值execute先把值替换到%s里然后给数据据发从此指令
            count += 1# 添加一本记一次
            if count % 20 == 0:# 每20本入库提交一次
                conn.commit()

conn.commit() #循环外：兜底提交最后不满 20 的那批
cursor.close()
conn.close()
print(f'完成，共入库 {count} 本')
