import tornado.web


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







