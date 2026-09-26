from flask import Flask
import pymysql
import pandas as pd

from sql_join_flask_config import DB_PASSWORD
# 需求：/top10 页面：展示最贵 10 本书，每本书显示【书名、价格、星级描述】
app = Flask(__name__)

@app.route('/top10')
def top10():
    # TODO 1：连接 MySQL
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd=DB_PASSWORD,
        database='books',
        charset='utf8mb4'
    )
    # TODO 2：执行 JOIN SQL（pd.read_sql）
    # 方式1直接sql语句查询
    data = pd.read_sql('''select bs.书名,bs.价格,sl.描述 from book_spider as bs
     join star_level as sl on bs.星标数=sl.星级名称 order by 价格 desc limit 10 ''',conn)
    # 方式2pandas 处理
    # data = pd.read_sql('select * from book_spider', conn)  # 书表，只搬原始数据
    # star = pd.read_sql('select * from star_level', conn)  # 星级字典表
    #
    # top10 = (data
    #          .merge(star, left_on='星标数', right_on='星级名称')  # = join … on
    #          [['书名', '价格', '描述']]  # = select 三列
    #          .sort_values('价格', ascending=False)  # = order by desc
    #          .head(10))  # = limit 10

    # TODO 3：关连接
    conn.close()
    # TODO 4：遍历结果，拼 HTML 展示（书名 - 价格 - 描述）
    html= ''
    rows = data.to_dict('records')
    for i in rows:
        html+= f'''<p>书名：{i['书名']} </p>
               <p> 价格：{i['价格']}</p> 
               <p> 描述：{i['描述']}</p> '''
    return html
# /评分       评分分布图（rating.png）
@app.route('/评分')
def rating():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd=DB_PASSWORD,
        database='books',
        charset='utf8mb4'
    )
    # 直接 拿到 数字星级 好 排 序 展 示
    data = pd.read_sql("""select sl.星级数字,count(*) as 数量 from book_spider as bs join star_level as sl on bs.星标数=sl.星级名称
     group by bs.星标数,sl.星级数字 order by sl.星级数字 limit 10 """,conn)

    conn.close()
    # 必须转格式！ conn.close()直接放 DataFrame 到 HTML 里会显示成一整块乱糟糟的表格。
    html = ''
    #  SQL 里已经 ORDER BY sl.星级数字 排好了
    # 排序放 pandas 里：sort_values('列名') —— 也行，但要先把乱序数据整个搬过来再排
    # rows = data.sort_index()  ##type:--> DataFrame  # 将星标数字排序  错误示例 它只排’索引‘
    for row in data.to_dict('records'):# 转字典
        html += f'<p>星级：{row["星级数字"]}，数量：{row["数量"]}</p>'
    return f'''
    <html>
    <body>
        <h1>评分数量概览：</h1>
        {html}
        <h1>评分分布图展示</h1>
        <img src="/static/rating.png" width="600">
    </body>
    </html>
    '''

# /库存       库存分布图（stock.png）
@app.route('/库存')
def img2():
    return f'''
<html>
<body>
    <h1>库存展示图</h1>
    <img src="/static/stock.png" width="600">

</body>
</html>
    '''
# 主页
@app.route('/')
def index():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd=DB_PASSWORD,
        database='books',
        charset='utf8mb4'
    )
    data = pd.read_sql("SELECT AVG(价格) as 平均价格  FROM book_spider",conn)
    conn.close()

    # rows = data.to_dict('records')# 不在用转字典
                # 取列           取行|
    avg_price = data['平均价格'].iloc[0]  # 从列表嵌套字典中取出数字，也就是value
#        平均价格
# 0       54.23     ← .iloc[0] 取这一行

    return f'''
<html>
<body style="background:#f5f5f5; font-family:微软雅黑; text-align:center">

    <h1>平均价格为：<b>{avg_price:.2f}</b></h1>
    <a href="/评分">点击链接查看评分</a><br><br>
    <a href="/库存">点击链接查看库存</a><br><br>
    <a href="/top10">点击链接查看最贵top10</a>
</body>
</html> 

    '''
app.run()
# 爬虫 → 数据 → 数据库 → Web → 作品上线
# （全链路打通，能投简历）