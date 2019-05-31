#websocket双向通信
import uuid
import tornado.websocket
import tornado.web
import tornado.escape   #解码message的jion格式
from datetime import datetime         #时间戳
from .main import BaseHandler
from pycket.session import SessionMixin

def make_da(handler,msg,username):                                                              #生成用了发送消息的字典
    chat = {  # 渲染html
        'id': str(uuid.uuid4()),
        'body': msg,
        'username': username,
        'created': str(datetime.now()),
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

    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def open(self, *args, **kwargs):                                                          #新的websocket 连接打开 自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.add(self)                                                          #连接打开就把信息加到里面

    def on_close(self):                                                                           #websocket连接断开  自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.remove(self)                                                         #连接断开就移除掉

    def on_message(self, message):                                                                 #websocket服务器接收到消息自动调用
        print('get message: {}'.format(message))
        par = tornado.escape.json_decode(message)                                                 #把发送的信息解码成json格式
        msg = par['body']

        chat = make_da(self,msg,self.current_user)
        self.send_upda(chat)
        self.updata(chat)

    def send_upda(self,chat):             #把新消息更新到hisoy里面，截取最后20条消息
        ChatWSHandler.history.append(chat['html'])                                                 #把历史消息增加到html
        if len(ChatWSHandler.history) > ChatWSHandler.history_size:
            ChatWSHandler.history = ChatWSHandler.history[-ChatWSHandler.history_size:]


    def updata(self,chat):
        for w in ChatWSHandler.waiters:
            w.write_message(chat)         #write_message负责把信息发送出去，给每个用户发送新消息


class EchoWebSocket(tornado.websocket.WebSocketHandler):               #服务端
    def open(self):                         #新的websocket 连接打开 自动调用
        print("WebSocket opened")

    def on_message(self, message):          #websocket连接断开  自动调用
        self.write_message(u"You said: " + message)

    def on_close(self):                      #websocket 服务队接收到消息自动调用
        print("WebSocket closed")