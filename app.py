#项目
import logging  #日志模块

import tornado.ioloop
import tornado.web

from hander1.main import IndexHandler,ExploreHandler,PostHandler#选中要放外部的类按f6，在里面选，引入外部的main文件
from hander1 import main,account,chat,yibu          #用户注册用的
from utils import uimethods,uimodules #导入外部包

import tornado.options                      #显示额外的信息1
from tornado.options import define,options  #调式模式 可以改变端口1

logging.basicConfig(level=logging.DEBUG,format='%(levelname)s -- %(funcName)s -- %(lineno)d -- %(filename)s: %(message)s')   #第一个是打印日志级别数值 第二个是当前函数   第三个是输出消息

define('port',default='8000',help='listening port',type=int)
define('debuh',default='True',help='Debug mode',type=bool)

class Application(tornado.web.Application):
    def __init__(self): #1
        hanlders = [
            (r'/', IndexHandler),
            (r'/explore', ExploreHandler),                #是数据库的图片页面
            (r'/post/(?P<post_id>[0-9]+)', PostHandler),  #？P是大写的，是Python里面用正则命名捕获的id ,在url里面添加的数字可以在要么显示
            (r'/signup', account.RegisterHandler),                        #数据库-用户注册页面1
            (r'/login', account.LoginHanlder),                            #数据库-用户登录页面的认证2
            (r'/upload', main.UploadHandler),                             #添加图片保存到数据库3
            (r'/logan', account.LogouHander),                             #退出登陆页面     第十二章
            (r'/profile', main.ProfileHandler),                           # 喜欢和收藏页面  第十三章
            (r'/like', main.LikeHandler),                                 # 喜欢和收藏页面点击  第十三章
            (r'/room', chat.RoomHandler),                                 #websocket双向通信    第十四章1
            (r'/ws/echo', chat.EchoWebSocket),                            #websocket双向通信 客服端    第十四章1
            (r'/ws', chat.ChatWSHandler),                                 #websocket双向通信 服务端   第十四章1
            (r'/guang', account.ExtendsHandler),                          #w弹窗广告   第十四章1
            (r'/syn', yibu.SyncSaveHandler),                          #w 第十五章  同步
            (r'/save', yibu.AsyncSaveHandler),                          #w 第十五章  异步
        ]
        settings = dict(
            debug=True,                        # 访问不存在的会报错1
            template_path='templates',         # 配置模板文件的名字是新创建的文件夹的名字一样
            static_path='static',              # 静态文件配置 自动去查找那个文件
        cookie_secret="wsegehdsg" ,            #随便输入字符串，好让别人看不见，预防用户伪造cookie
        login_url='/login',                    #用cxtends访问页面,重定向跳转 到login登录页面
        ui_methods=uimethods,         #一个函数或类需要在很多模板中被导入
        ui_modules=uimodules,         #一个函数或类需要在很多模板中被导入
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
