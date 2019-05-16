#db查询的模块的辅助函数
from models.auth import User,Session

def auto(username,password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()    #查询用户的密码在数据库里有匹配的记录，query查询User，filter_by不用等等于符号，是用传参形式查询，first是取第一个元素
    return User.get_password(username) == password  #调用get_password函数的username是否等于password