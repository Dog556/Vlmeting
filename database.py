import sqlite3

def create_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY,
            title TEXT,
            up_time TEXT,
            msg TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()

def insert_data(data):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for item in data:
        c.execute('''
            INSERT INTO vulnerabilities (title, up_time, msg, url) VALUES (?, ?, ?, ?)
        ''', (item['title'], item['up_time'], item['msg'], item['url']))
    conn.commit()
    conn.close()

def url_exists(url):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM vulnerabilities WHERE url = ?', (url,))
    return c.fetchone() is not None

def insert_unique_data(data):
    new_inserted = []
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for item in data:
        if not url_exists(item['url']):
            c.execute('''
                INSERT INTO vulnerabilities (title, up_time, msg, url) VALUES (?, ?, ?, ?)
            ''', (item['title'], item['up_time'], item['msg'], item['url']))
            new_inserted.append(item)  # 添加到新插入的数据列表
    conn.commit()
    conn.close()
    return new_inserted


def db_json():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT title, up_time, msg, url FROM vulnerabilities')
    rows = c.fetchall()
    # 将每行数据转换为字典，并排除id字段
    data = []
    for row in rows:
        # 排除id字段，只包含需要的数据
        entry = {
            'title': row[0],
            'up_time': row[1],
            'msg': row[2],
            'url': row[3]
        }
        data.append(entry)
    # 将字典列表转换为JSON字符串
    conn.close()
    return data

# 清除数据
def clear_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # 删除表中的所有数据，但保留表结构
    c.execute('DELETE FROM vulnerabilities')
    conn.commit()
    conn.close()


def check_data_exists_in_db(web_data, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 遍历Web请求的JSON数据
    for item in web_data:
        query = 'SELECT 1 FROM vulnerabilities WHERE url = ?'
        c.execute(query, (item['url'],))

        # 如果查询结果为空，则数据不存在，返回False
        if c.fetchone() is None:
            conn.close()  # 关闭数据库连接
            return False

    # 如果所有数据都存在于数据库中，返回True
    conn.close()  # 关闭数据库连接
    return True
