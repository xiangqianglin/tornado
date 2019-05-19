#db查询的模块的辅助函数
import hashlib     #用做  md5  密码加密
from models.auth import User,Post
from models.db import Session

def hasheb(text):                                     #接收的是文本,这里可以加盐
    return hashlib.md5(text.encode('utf8')).hexdigest()

def auto(username,password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()    #查询用户的密码在数据库里有匹配的记录，query查询User，filter_by不用等等于符号，是用传参形式查询，first是取第一个元素
    return User.get_password(username) == hasheb(password)             #调用get_password函数的username是否等于password

def register(username,password):                                     #辅助函数，提交用户和密码
    s = Session()
    s.add(User(username=username,password=hasheb(password)))         #密码加密
    s.commit()
    s.close()

def add_post(image_url,thumb_url,username):                                    #把上传的图片保存到数据库,增加thumb_url字段保存到数据库
    s = Session()
    user = s.query(User).filter_by(username=username).first()
    post = Post(image_url=image_url,thumb_url=thumb_url,user=user)   #增加字段的返回添加到数据库
    s.add(post)
    s.commit()
    post_id = post.id
    s.close()

    return post_id

def get_all_posts():                                                #显示所有图片信息
    session = Session()
    posts = session.query(Post).all()
    return posts

def get_post(post_id):                                             #拿单个post图片的信息
    session = Session()
    post = session.query(Post).filter_by(id=post_id).first()
    return post