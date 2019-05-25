#db查询的模块的辅助函数
import hashlib     #用做  md5  密码加密
from models.auth import User,Post,Likeg
from models.db import Session

def hasheb(text):                                     #接收的是文本,这里可以加盐
    return hashlib.md5(text.encode('utf8')).hexdigest()

def auto(username,password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()    #查询用户的密码在数据库里有匹配的记录，query查询User，filter_by不用等等于符号，是用传参形式查询，first是取第一个元素
    return User.get_password(username) == hasheb(password)             #调用get_password函数的username是否等于password

class HandlerORM:                                                    #辅助操作数据库的工具类，结合RequestHabdler使用
    def __init__(self,db_session):                                   #由handler 进行实例化和close
        self.db = db_session

    def get_post(self, post_id):                                     # 返回特定id的post实例
        post = self.db.query(Post).filter_by(id=post_id).first()
        return post

    def get_user(self, username):                                    #有几个都用这个方法，就可以提取出来简化代码
        user = self.db.query(User).filter_by(username=username).first()
        return user

    def register(self,username,password):                                     #辅助函数，提交用户和密码
        self.db.add(User(username=username,password=hasheb(password)))         #密码加密
        self.db.commit()

    def add_post(self,image_url,thumb_url,username):                                    #把上传的图片保存到数据库,增加thumb_url字段保存到数据库
        user = self.get_user(username)
        post = Post(image_url=image_url,thumb_url=thumb_url,user=user)       #增加字段的返回添加到数据库
        self.db.add(post)
        self.db.commit()
        post_id = post.id

        return post_id

    def get_all_posts(self):                                                #显示所有图片信息
        posts = self.db.query(Post).all()
        return posts

    def get_posts_for(self,username):                                       #拿单个post图片的信息
        user = self.get_user(username)
        posts = self.db.query(Post).filter_by(user=user).all()
        return posts




    def likeg_posts_for(self,username):                                    #查询用户喜欢的posts图片 第十三章
        user = self.get_user(username)
        post = self.db.query(Post).filter(Post.id == Likeg.post_id,        #查询多个
                                          Likeg.post_id == user.id,
                                          Post.user_id != user.id)         #自己上传的要是喜欢的就不要显示
        return post

    def count_like_for(self,post_id):                                     #查询有哪些用户喜欢这个图片
        count = self.db.query(Likeg).filter_by(post_id=post_id).count()
        return count





















