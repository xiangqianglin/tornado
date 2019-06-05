#websocket双向通信
import uuid
import tornado.websocket
import tornado.web
import tornado.gen
import tornado.escape   #解码message的jion格式
import logging          #日志输出
from datetime import datetime         #时间戳
from .main import BaseHandler
from pycket.session import SessionMixin
from tornado.httpclient import AsyncHTTPClient        #处理消息中的URL
from tornado.ioloop import IOLoop      #spawn callback方式的异步保存图片

logger = logging.getLogger('tudo.log')             #名字是统一的随意的

def make_da(handler,msg,username='system',img_url=None,post_id=None):                                    #生成用了发送消息的字典
    chat = {  # 渲染html
        'id': str(uuid.uuid4()),
        'body': msg,
        'username': username,
        'created': str(datetime.now()),
        'img_url': img_url,
        'post_id': post_id,
    }
    chat['html'] = tornado.escape.to_basestring(handler.render_string('message.html', chat=chat))
    return chat

class RoomHandler(BaseHandler):                 #聊天室页面
    @tornado.web.authenticated
    def get(self):
        self.render('room.html',messages=ChatWSHandler.history)                                  #messages传入历史消息

class ChatWSHandler(tornado.websocket.WebSocketHandler,SessionMixin):                                        #处理和响应 websocket 连接的  客服端
    waiters = set()                                                                            #等待接受信息的用户
    history = []                                                                                 #存放历史消息   类属性
    history_size = 20                                                                            #存放最后20条历史消息   类属性

    def check_origin(self, origin: str):
        return True

    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def open(self, *args, **kwargs):                                                          #新的websocket 连接打开 自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.add(self)                                                          #连接打开就把信息加到里面

    def on_close(self):                                                                           #websocket连接断开  自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.remove(self)                                                         #连接断开就移除掉

    @tornado.gen.coroutine
    def on_message(self, message):                                                                 #websocket服务器接收到消息自动调用
        print('get message: {}'.format(message))
        par = tornado.escape.json_decode(message)                                                 #把发送的信息解码成json格式
        msg = par['body']

        if msg and msg.startswith('http://'):                                          #用户输入的是url，就判断输入的以什么开头#####
            client = AsyncHTTPClient()                                                 #处理url的库


            # resp = yield client.fetch(msg)                                          #第一种异步调用方法，这种异步要等待结果
            # chat = make_da(self,msg)



            save_api_url = "http://192.168.80.130:8000/save?save_url={}&name={}".format(msg,self.current_user) #第二种异步调用方法，这种异步不用等待
            logger.info(save_api_url)                                                  #查看平凑的url
            IOLoop.current().spawn_callback(client.fetch,
                                            save_api_url,
                                            request_timeout=30)                        #发起一个回调，延迟时间，这个是一劳永逸的异步抓取操作
            repply_msg = "user {} url {} is proc,".format(self.current_user,msg)        #给用户返回消息,插入用户名和url

            chat = make_da(self,repply_msg)                                           #系统返回的消息
            self.write_message(chat)                                                  #这样就是发送给所有用户都能看见

        else:                                                                         #用户输入的不是url的就这样给聊天室发送消息###############
            chat = make_da(self,msg,self.current_user)
            ChatWSHandler.send_upda(chat)                                             #用了装饰器就用类的方法名去调用
            ChatWSHandler.updata(chat)

    @classmethod
    def send_upda(cls,chat):             #把新消息更新到hisoy里面，截取最后20条消息,用了类的装饰器，就用cls
        ChatWSHandler.history.append(chat['html'])                                                 #把历史消息增加到html
        if len(ChatWSHandler.history) > ChatWSHandler.history_size:
            ChatWSHandler.history = ChatWSHandler.history[-ChatWSHandler.history_size:]

    @classmethod
    def updata(cls,chat):
        for w in ChatWSHandler.waiters:
            w.write_message(chat)         #write_message负责把信息发送出去，给每个用户发送新消息


class EchoWebSocket(tornado.websocket.WebSocketHandler):               #服务端
    def open(self):                         #新的websocket 连接打开 自动调用
        print("WebSocket opened")

    def on_message(self, message):          #websocket连接断开  自动调用
        self.write_message(u"You said: " + message)

    def on_close(self):                      #websocket 服务队接收到消息自动调用
        print("WebSocket closed")