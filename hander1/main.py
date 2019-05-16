import tornado.web
from pycket.session import SessionMixin  #添加session的一些功能的类

class BaseHandler(tornado.web.RequestHandler,SessionMixin):  #所有需要跳转回访问页面的类都可以继承这个
    def get_current_user(self):   #复写current_user方法来 用户认证
        # return self.get_secure_cookie('tudo_cookie',None)  #返回设置cookie的名字，拿不到就返回空
        return self.session.get('tudo_user',None)  #用session去拿tudo_user，拿不到就返回空

class IndexHandler(tornado.web.RequestHandler):  #所有需要跳转回访问页面的类都可以继承这个
    def get(self):
        self.render('index1.html')

class ExploreHandler(tornado.web.RequestHandler):#最近上传的图片页面
    def get(self):
        self.render('explore2.html')

class PostHandler(tornado.web.RequestHandler): #单个图片详情页面
    def get(self,post_id):
        self.render('post.html',post_id=post_id)

    # def get(self,*args,**kwargs):  #这样可以命名捕获任意的数字
    #     self.render('post.html',post_id=kwargs['post_id'])







