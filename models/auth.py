#创建models模板
from datetime import datetime  #时间库
from sqlalchemy import Column, Integer, String, DateTime  #用于创建表的中间件sqlalchemy，

from models.db import Base                   #引入models模块里面的Base类型

class User(Base):                          #创建表的信息
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)#限制：primart_key是唯一，autoincrement是自增长
    username = Column(String(50),unique=True,nullable=False)#限制：unique是主键，nullable是不能为空
    password = Column(String(50))
    creatime = Column(DateTime,default=datetime.now)

if __name__ == '__main__':
    Base.metadata.create_all()  #执行create_all方法就会去找对应的类在去创建表





