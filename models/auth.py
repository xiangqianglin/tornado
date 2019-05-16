#创建models模板
from datetime import datetime                                                #时间库
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey          #用于创建表的中间件sqlalchemy，
from sqlalchemy.orm import relationship                                      #relationship是关系管理型的mode模块
from sqlalchemy.sql import exists                                            #20行  exists是SQL里面的查询 返回的结果是Tree或者Fells
from models.db import Base,Session                                           #引入models模块里面的Base类型和Session

session = Session()
class User(Base):                                                            #创建用户表的信息  一个一会对应多个post关系
    __tablename__ = 'users'                                                  #这个user可以随意   《数据库表名》
    id = Column(Integer,primary_key=True,autoincrement=True)                 #限制：primart_key是主键，autoincrement是自增长  《创建表中的字段》
    username = Column(String(50),unique=True,nullable=False)                 #限制：unique是唯一，nullable是不能为空    《整类型的长度》
    password = Column(String(50))                                            #《字符类型的长度》
    creatime = Column(DateTime,default=datetime.now)                         #《时间类型》
    # email = Column(String(80))                                             #增加邮件字段

    def __repr__(self):
        return "<User:#{}-{}>".format(self.id, self.username)                    #字符串显示的格式

    @classmethod
    def is_exis(cls,username):                                      #接收一个参数，查询一个参数好认证是否存在
        return session.query(exists().where(cls.username == username)).scalar()  #scalar这个也是查询，把结果向量化，获取他的实际值

    @classmethod
    def get_password(cls,username):                                      #接收两个参数，查询两个参数好认证是否存在
        user = session.query(cls).filter_by(username=username).first()       #查询不到就返回一个空
        if user:
            return user.password
        else:
            return ''


class Post(Base):                                                            #创建提交  一个一会对应多个post关系
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))  #图片

    user_id = Column(Integer,ForeignKey('users.id'))                           #ForeignKey是与外部连接关系的关键字
    user = relationship('User',backref='posts',uselist=False,cascade='all')   #relationship是关系管理型的mode模块


    def __repr__(self):
        return "<post:#{}-{}>".format(self.id, self.name)                    #字符串显示的格式


if __name__ == '__main__':
    Base.metadata.create_all()                                               #执行create_all方法就会去找对应的类在去创建表





