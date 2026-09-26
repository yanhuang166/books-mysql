"""
Python 连接 MySQL（pymysql）
查出数据（SQL 自己写）
处理数据（注意：库存字段是 "In stock (22 available)" 这种文本，要提取出数字）
matplotlib 画柱状图 + 标题 + 坐标轴
保存成 库存分布_mysql.png
"""
# 1:Python 连接 MySQL（pymysql）
import pymysql
import pandas as pd
conn = pymysql.connect(
    host='localhost',# 主机地址：本机
    port=3306,# 端口号
    user='root',# 用户名
    passwd=input('请输入密码：'),# 连接数据库密码
    database='books',# 选择数据库
    charset='utf8mb4'
)
# 查出数据（SQL 自己写）cursor是写入数据库

data=pd.read_sql('select * from book_spider  ',conn)
# print(data)
# 处理数据（注意：库存字段是 "In stock (22 available)" 这种文本，要提取出数字）   value_counts 按「值（本数）」排
stock=data['库存'].str.extract(r'(\d+)',expand=False).astype(int).value_counts().sort_index()
# print(stock)
# matplotlib 画柱状图 + 标题 + 坐标轴
from matplotlib import pyplot
pyplot.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #
pyplot.rcParams['axes.unicode_minus'] = False

stock.plot(kind='bar',x='库存',y='数量（本）')
pyplot.title('库存分布')
pyplot.savefig('库存分布_mysql.png')
pyplot.show()
conn.close() # 结束连接