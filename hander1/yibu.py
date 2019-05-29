#异步应用
import time
import logging

import requests

from tornado.httpclient import AsyncHTTPClient                    #阻塞的类
from tornado.gen import coroutine, sleep                          #coroutine装饰器

from .main import BaseHandler
from utils.photo import UploadImage


logger = logging.getLogger('tudo.log')                                      #打印操作顺序的日志和时间戳

class SyncSaveHandler(BaseHandler):                                         #同步

    def get(self):
        logger.info(self)
        save_url = self.get_argument('save_url', '')                         #请求图片，在save_url后面提交图片网址
        logger.info(save_url)

        resp = requests.get(save_url)                                        #在用requests下载下来，，这里加载很慢，就是I O阻塞
        time.sleep(15)

        logger.info(resp.status_code)                                        #status_code是返回状态码
        up_img = UploadImage('qiang.jpg', self.settings['static_path'])       #用辅助函数在静态路径拿到图片，保存图片名字是qiang
        up_img.save_upload(resp.content)                                      #保存图片方法，  content是图片数据内容
        up_img.make_thumb()                                                   #生成缩略图

        post_id = self.orm.add_post(up_img.image_url,                         #保存图片到数据库的方法
                                    up_img.thumb_url,
                                    self.current_user)

        self.redirect('/post/{}'.format(post_id))                            #跳转


class AsyncSaveHandler(BaseHandler):                                       #异步出来I/O阻塞要用异步    用协
    @coroutine                                                             #Python内置的异步装饰器是async    await相当于yield
    def get(self):
        save_url = self.get_argument('save_url', '')
        logger.info(save_url)

        client = AsyncHTTPClient()                                     #同步用requests，异步用AsyncHTTPClient去下载图片
        resp = yield client.fetch(save_url)                            #用client装饰器标记这个函数，在用yield把这个结果抛出来，执行到这里会暂停   《****重要****》
        logger.info(resp.code)
        yield sleep(20)                                               #时间延迟
        logger.info('sleep end')

        up_img = UploadImage('x.jpg', self.settings['static_path'])
        up_img.save_upload(resp.body)
        up_img.make_thumb()

        post_id = self.orm.add_post(up_img.image_url,
                                    up_img.thumb_url,
                                    self.current_user)

        self.redirect('/post/{}'.format(post_id))

#http://pic1.win4000.com/wallpaper/2018-05-08/5af150aea45bd.jpg
#http://192.168.80.130:8000/syn?save_url=http://pic1.win4000.com/wallpaper/2018-05-08/5af150aea45bd.jpg     是在网页刷新
#http://192.168.80.130:8000/syn?save_url=http://source.unsplash.com/random  是用同步生成随机图片
#http://192.168.80.130:8000/save?save_url=http://source.unsplash.com/random  这个是用异步生成随机图片



