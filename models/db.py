#连接数据库
from sqlalchemy import create_engine  #连接数据库
from sqlalchemy.ext.declarative import declarative_base #创建Models库要用的
from sqlalchemy.orm import sessionmaker  #创建会话库

HOST = '192.168.80.130'
PORT = '3306'
DATABASE = 'tudo36'   #这个是数据库创建的库名
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOST,PORT,DATABASE
)

engine = create_engine(DB_URI)  #连接数据库 1

Base = declarative_base(engine)   ##创建Models库要用的 2

Session = sessionmaker(bind=engine)  #绑定一个引擎来创建数据库会话类 3

if __name__ == '__main__':
    connection = engine.connect()#连接数据库
    result = connection.execute('select 1')#输出的内容
    print(result.fetchone())


