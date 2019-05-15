#创建models模板
from datetime import datetime                                                #时间库
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey          #用于创建表的中间件sqlalchemy，
from sqlalchemy.orm import relationship                                      #relationship是关系管理型的mode模块
from models.db import Base,Session                                                 #引入models模块里面的Base类型和Session

class User(Base):                                                            #创建用户表的信息  一个一会对应多个post关系
    __tablename__ = 'users'                                                  #这个user可以随意   《数据库表名》
    id = Column(Integer,primary_key=True,autoincrement=True)                 #限制：primart_key是主键，autoincrement是自增长  《创建表中的字段》
    username = Column(String(50),unique=True,nullable=False)                 #限制：unique是唯一，nullable是不能为空    《整类型的长度》
    password = Column(String(50))                                            #《字符类型的长度》
    creatime = Column(DateTime,default=datetime.now)                         #《时间类型》
    # email = Column(String(80))                                             #增加邮件字段

    def __repr__(self):
        return "<User:#{}-{}>".format(self.id, self.name)                    #字符串显示的格式

class Post(Base):                                                            #创建提交  一个一会对应多个post关系
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))  #图片

    user_id = Column(Integer,ForeignKey('users.id'))                           #ForeignKey是与外部连接关系的关键字
    user = relationship('User',backref='posts',uselist=False,cascade='all')   #relationship是关系管理型的mode模块


    def __repr__(self):
        return "<post:#{}-{}>".format(self.id, self.name)                    #字符串显示的格式

def register(username,password):                                             #辅助函数，提交用户和密码
    s = Session()
    s.add(User(username=username,password=password))
    s.commit()
if __name__ == '__main__':
    Base.metadata.create_all()                                               #执行create_all方法就会去找对应的类在去创建表





