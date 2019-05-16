#项目
import tornado.ioloop
import tornado.web

from hander1.main import IndexHandler,ExploreHandler,PostHandler#选中要放外部的类按f6，在里面选，引入外部的main文件
from hander1 import main,account            #用户注册用的

import tornado.options                      #显示额外的信息1
from tornado.options import define,options  #调式模式 可以改变端口1
define('port',default='8000',help='listening port',type=int)
define('debuh',default='True',help='Debug mode',type=bool)

class Application(tornado.web.Application):
    def __init__(self): #1
        hanlders = [
            (r'/', IndexHandler),
            (r'/explore', ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),  #？P是大写的，是Python里面用正则命名捕获的id ,在url里面添加的数字可以在要么显示
            (r'/signup', account.RegisterHandler),                        #数据库-用户注册页面1
            (r'/login', account.LoginHanlder),                            #数据库-用户登录页面的认证2
            (r'/upload', main.UploadHandler),                             #图片保存到数据库3
        ]
        settings = dict(
            debug=True,                        # 访问不存在的会报错1
            template_path='templates',         # 配置模板文件的名字是新创建的文件夹的名字一样
            static_path='static',              # 静态文件配置 自动去查找那个文件
        cookie_secret="wsegehdsg" ,            #随便输入字符串，好让别人看不见，预防用户伪造cookie
        login_url='/login',                    #用cxtends访问页面,重定向跳转 到login登录页面
        # xsrf_cookies=True,                   #跨站请求防御***
        pycket = {                             #这个是用session登陆用的
            'engine': 'redis',                 #使用redis这个引擎，存储session数据
            'storage': {
                'host': 'localhost',           #用localhost去连接127.0.0.1这个地址
                'port': 6379,                  #端口是6379
                # 'password': '',              #有密码就要加
                'db_sessions': 5,              #redis db index   redis的第五个db位置
                # 'db_notifications': 11,      #可以不用
                'max_connections': 2 ** 30,    #储存最大连接数
            },
            'cookies': {
                'expires_days': 30,  #过期时间
            },
        }
        )
        super().__init__(hanlders,**settings)  #super就是调用父类的方法，setting都是关键字，要用**来解包

application = Application()  # 实例化类

if __name__ == "__main__":
    tornado.options.parse_command_line()  #1
    # application = Application(debug=options.debug)  # 实例化类  ,这样加debug可以不会提示错误信息1
    application.listen(options.port) #listen是对指定计算机监听端口1
    print("server{}".format(str(options.port)))    #1
    tornado.ioloop.IOLoop.current().start()  #  IOLoop是重复启动IO 启动tornado用start

    # application.listen(8000) #listen是对指定计算机监听端口
    # print("server{}".format('8000'))
    # tornado.ioloop.IOLoop.current().start()  #  IOLoop是重复启动IO 启动tornado用start
