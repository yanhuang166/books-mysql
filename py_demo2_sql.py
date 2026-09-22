# 9.22自主

# 需求：画出"每个星级的平均库存"柱状图

# 需求分析：1: x轴（横轴）是星级具体有one柱tow柱直到five.
# 2:纵轴y:一类星级的平均数
# 3:五个柱状图
# 4：需要处理，库存是文本，处理流程是：先转字符串然后extract(搭配正则expand=False)提取数字文本，之后用astype(int)转数字然后就能算平均值了（.mean()）


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
# 读取数据，
data=pd.read_sql('select * from book_spider  ',conn)
# print(data.head())# 先看数据面貌   貌似看不了  ->              详情页URL  ...                                                 简介
# 0  https://books.toscrape.com/catalogue/a-light-i...  ...  It's hard to imagine a world without A Light i...

# 取所需数据
star=data['星标数']
stock = data['库存'].str.extract(r'(\d+)',expand=False).astype(int)# 提取数据
data['库存'] = stock # 重新给dataframe赋值
price = data.groupby('星标数')['库存'].mean() # 每颗星平均库存
price=price.reindex(['One','Two','Three','Four','Five'])# 索引排序
# 上图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] #
plt.rcParams['axes.unicode_minus'] = False
price.plot(kind='bar')
plt.title('星级的平均库存')
plt.savefig('平均库存_mysql.png')
plt.show()

conn.close()