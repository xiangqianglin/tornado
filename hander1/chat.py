#websocket双向通信
import uuid
import tornado.websocket
import tornado.web
import tornado.escape   #解码message的jion格式
from .main import BaseHandler

class RoomHandler(BaseHandler):                 #聊天室页面
    @tornado.web.authenticated
    def get(self):
        m = {
            'id':2354,
            'username':self.current_user,
            'body':'hello'
        }
        msg = [
            {
                'html':self.render_string('message.html',chat=m)
            }
        ]
        self.render('room.html',messages=msg)

class ChatWSHandler(tornado.websocket.WebSocketHandler):                                        #处理和响应 websocket 连接的  客服端
    waiters = set()                                                                            #等待接受信息的用户

    def open(self, *args, **kwargs):                                                          #新的websocket 连接打开 自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.add(self)                                                          #连接打开就把信息加到里面

    def on_close(self):                                                                           #websocket连接断开  自动调用
        print('close ws connect:{}'.format(self))
        ChatWSHandler.waiters.remove(self)                                                         #连接断开就移除掉

    def on_message(self, message):                                                                 #websocket 服务队接收到消息自动调用
        print('get message: {}'.format(message))
        par = tornado.escape.json_decode(message)                                                 #把发送的信息解码成json格式
        msg = par['body']
        chat = {
            'id':str(uuid.uuid4()),
            'body':msg,
            'username':'username'
        }
        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html',chat=chat))
        for w in ChatWSHandler.waiters:
            w.write_message(chat)         #write_message负责把信息发送出去

class EchoWebSocket(tornado.websocket.WebSocketHandler):               #服务端
    def open(self):                         #新的websocket 连接打开 自动调用
        print("WebSocket opened")

    def on_message(self, message):          #websocket连接断开  自动调用
        self.write_message(u"You said: " + message)

    def on_close(self):                      #websocket 服务队接收到消息自动调用
        print("WebSocket closed")