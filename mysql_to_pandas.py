# 导
import pandas as pd
import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    port=3306,
    password=input('请输入密码'),
    database='books',
    user='root',
    charset='utf8'
)
# 数据查询
# df = pd.read_sql('select * from book', conn)

#
# print(df.head())
# print(df.dtypes)
# print(df.shape)

#SQL 聚合 → pandas → 画图

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ① SQL 负责聚合（GROUP BY 在数据库里干）
df_star = pd.read_sql("""SELECT 星标数, AVG(价格) AS 均价
 FROM book GROUP BY 星标数  ORDER BY FIELD(星标数, 'One', 'Two', 'Three', 'Four', 'Five')""", conn)
print(df_star) # 顺序是乱的

# ② pandas 接收 → matplotlib 画图（你会）
df_star.plot(kind='bar', x='星标数', y='均价')
plt.title('各星级平均价格')
plt.savefig('星级均价.png')
plt.show()
conn.close() # 结束连接
