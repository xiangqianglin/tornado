#处理账号相关的模块
import tornado.web
from models.auth import register                               #引入models文件下面auth。py里面的register函数

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')  #提交用户和密码信息
    def post(self):                   #
        username = self.get_argument('username','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        if username and password1 and (password1 == password2):  #判断username和password不是空的还有1和2相等，就运行注册
            register(username,password1)
            self.write('注册成功')
        else:
            self.write('bab username/password')                  #跳转到输出信息