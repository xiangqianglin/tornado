import tornado.web
from pycket.session import SessionMixin  #添加session的一些功能的类
from utils.photo import UploadImage
from PIL import Image  #图片处理
from utils.account import HandlerORM  #数据库的图片调用
from models.db import Session

class BaseHandler(tornado.web.RequestHandler,SessionMixin):  #所有需要跳转回访问页面的类都可以继承这个
    def get_current_user(self):   #复写current_user方法来 用户认证
        # return self.get_secure_cookie('tudo_cookie',None)  #返回设置cookie的名字，拿不到就返回空
        return self.session.get('tudo_user',None)  #用session去拿tudo_user，拿不到就返回空

    def prepare(self):                             #准备操作生命周期
        self.db_session = Session()
        self.orm = HandlerORM(self.db_session)

    def on_finish(self):
        self.db_session.close()                    #结束操作生命周期

class IndexHandler(BaseHandler):  #首页 用户上传图片的展示
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for(self.current_user)                  #在数据库查询图片出来
        self.render('index1.html',posts=posts)   #在网页展示

class ExploreHandler(BaseHandler):#最近上传的缩略图页面
    def get(self):
        posts = self.orm.get_all_posts()
        self.render('explore2.html',posts=posts)

class PostHandler(BaseHandler): #单个图片详情页面
    def get(self,post_id):
        post = self.orm.get_post(post_id)           #在数据库查询单个图片出来
        user = post.user
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
            self.render('post.html',post=post,user=user)     #在网页展示

class ProfileHandler(BaseHandler):                          #用户档案页面 第十三章  添加喜欢的图片
    @tornado.web.authenticated
    def get(self):
        user = self.orm.get_user(self.current_user)          #拿到用户的
        self.render('profile.html',user=user,like_posts=[])

class UploadHandler(BaseHandler):                                #上传图片  保存             7
    @tornado.web.authenticated                                 #用户认证过的才能访问
    def get(self):
        self.render("upload.html")                             #继承表单

    @tornado.web.authenticated                                 #用户认证过的才能访问
    def post(self):
        pics = self.request.files.get('picture',[])              #request是继承里面的，表单提交的数据放在files这个对象里面，这是拿数据的方法，它遍历名字(HTML 标签   picture和html文件里面的一样，拿不到picture就返回空)
        post_id = 1
        for p in pics:
            up_img = UploadImage(p['filename'],self.settings['static_path'])
            up_img.save_upload(p['body'])
            up_img.make_thumb()
            post_id = self.orm.add_post(up_img.image_url,
                                        up_img.thumb_url,  # 添加字段信息
                                        self.current_user)  # self.current_user是拿用户名的字段

        # self.write('提交成功')                                   #返回到网页的内容
        self.redirect('/post/{}'.format(post_id))                    #跳转到post.html




