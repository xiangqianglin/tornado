import tornado.web
from pycket.session import SessionMixin  #添加session的一些功能的类

from PIL import Image  #图片处理
from utils.account import add_post

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


class UploadHandler(BaseHandler):                                #上传图片  保存             7
    @tornado.web.authenticated                                 #用户认证过的才能访问
    def get(self):
        self.render("upload.html")                             #继承表单

    @tornado.web.authenticated                                 #用户认证过的才能访问
    def post(self):
        pics = self.request.files.get('picture',[])              #request是继承里面的，表单提交的数据放在files这个对象里面，这是拿数据的方法，它遍历名字(HTML 标签   picture和html文件里面的一样，拿不到picture就返回空)
        post_id = 1
        for p in pics:
            save_th = 'static/upload/{}'.format(p['filename'])   # 储存图片文件到路径里面
            with open(save_th, 'wb') as fh:                      #写入数据到save_th的路径里面
                fh.write(p['body'])                              #保存的数据，body是图片二级制数据

            post_id = add_post('upload/{}'.format(p['filename']),self.current_user)
            hah = Image.open(save_th)                           #生成缩略图
            hah.thumbnail((200,200))
            hah.save('static/upload/thumb_{}.jpg'.format(p['filename']),'JPEG')

        # self.write('提交成功')                                   #返回到网页的内容
        self.render('/post/{}'.format(post_id))                    #跳转到post.html  ========post_id找不到？？？？？？？？




