#生成缩略图文件
import os
from uuid import uuid4
from PIL import Image

class UploadImage(object):      #铺助保存用户上传的图片，生成对应的缩略图，记录图片相关的 URL  用来保存到数据库
    upload_dir = 'upload'  #
    thumb_dir = 'thumbs'    #缩略图存储的路径
    thumb_size = (200,200)  #缩略图的大小

    def __init__(self,name,static_path):
        self.new_name = self.gen_mew_name(name)
        self.static_path = static_path

    def gen_mew_name(self,name):                #生成新的唯一的字符串，用作图片名字
        _,ext = os.path.splitext(name)          # _,ext是切割1.jpg
        return uuid4().hex + ext                #uuid4会随机生成字符串，在。hex就只是纯粹的字符串，在加上jpg

    @property                                   #属性装饰器
    def image_url(self):                        #保存图片到数据库的相对地址，大图片***
        return os.path.join(self.upload_dir,self.new_name)

    @property
    def save_path(self):                        #这个路径在保存图片的时候会用和打开缩略图用《》
        return os.path.join(self.static_path,self.image_url)   #jion就是把里面参数连接起来生成路径,  上面用了属性装饰器，这里就可以不用调用，可以当属性拿来用就可以

    def save_upload(self,content):              #保存图片会用到上面这个方法，，content相当于body 《》
        with open(self.save_path, 'wb') as fh:  # 写入数据到save_th的路径里面
            fh.write(content)                   # 保存的数据，content是图片二级制数据

    @property
    def thumb_url(self):                        #保存图片到数据库的相对地址，小图片***
        name,ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(name,
                                         self.thumb_size[0],
                                         self.thumb_size[1],
                                         ext)
        return os.path.join(self.upload_dir,self.thumb_dir,thumb_name)

    def make_thumb(self):                       #生成缩略图文件《》
        hah = Image.open(self.save_path)        # 生成缩略图
        hah.thumbnail(self.thumb_size)
        save_path = os.path.join(self.static_path,self.thumb_url)  #保存的路径   static_path是静态目录
        hah.save(save_path, 'JPEG')            #保存的路径和格式  45:58