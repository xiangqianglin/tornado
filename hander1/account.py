#处理账号相关的模块
import tornado.web
from .main import BaseHandler
from utils.account import auto


class RegisterHandler(BaseHandler):   #注册
    def get(self):
        self.render('register.html')  #提交用户和密码信息
    def post(self):                   #
        username = self.get_argument('username','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        if username and password1 and (password1 == password2):  #判断username和password不是空的还有1和2相等，就运行注册
            self.orm.register(username,password1)
            self.session.set('tudo_user',username)
            self.redirect('/')                                  #redirect路径跳转到首页
        else:
            self.write('bab username/password')                  #跳转到输出信息

class LoginHanlder(BaseHandler):            #登陆
    def get(self):  # 设置cookie信息
        next_url = self.get_argument('next', '')  # 拿到post提交的这个只是希望在登录页面显示是用那个路由访问的，在html2里面设置  跳转回原来正在访问的 URL
        mai = self.get_argument('mai','')
        self.render('login.html',next_url=next_url,mai=mai)  # 告诉他外部的HTML文件在哪里，传入HTML的文件名

    def post(self):  # 表单接收
        username = self.get_argument('username','')       # 所有的表单都是用get_argument按键值来操作，有就传入下面模板里面的username，在html_2.html判断，提交了就输出里面的内容。。没有就返回no
        password = self.get_argument('password','')       # 所有的表单都是用get_argument按键值来操作，有就传入下面模板里面的username，在html_2.html判断，提交了就输出里面的内容。。没有就返回no
        next_url = self.get_argument('next', '')          # 所有的表单都是用get_argument按键值来操作，有就传入下面模板里面的username，在html_2.html判断，提交了就输出里面的内容。。没有就返回no

        if not username.split() or not password.split():  # 判断提交时其中一个是空的或者是空格
            self.redirect('/login?mai=密码或账号错误')  # 就跳转会登录页面
        else:
            if auto(username,password):                    #用utils.account import auto的函数来效验
                self.session.set("tudo_user",username)  # 设置cookie名字，在带上用户记住的可以在浏览器看见的qq：内容*********3
                if next_url:
                    self.redirect(next_url)  # 存在就跳转到next_url
                else:
                    self.redirect('/')  # 如果没有就跳转到首页
            else:
                self.redirect('/login?mai=账号或密码错误')  # 如果不是就跳转回要登录的状态

class LogouHander(BaseHandler):
    def get(self):
        self.session.delete("tudo_user")   #退出登陆用的删除会话信息
        self.render('logan.html')