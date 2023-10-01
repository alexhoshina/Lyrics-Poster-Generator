from PIL import Image, ImageDraw, ImageFilter

class Poster():
    """
    海报\n
    lyrics: 歌词\n
    singer: 歌手\n
    song_title: 歌曲名\n
    watermark: 水印\n
    size: 海报大小\n
    """
    def __init__(self, lyrics, singer, song_tiyle,
                 bg_image, cover_image, 
                 watermark, size):
        
        self.lyrics = lyrics # 歌词
        self.singer = singer # 歌手
        self.song_title = song_tiyle # 歌曲名
        self.watermark = watermark #水印

        self.text_dict = {
            "lyrics": self.lyrics,
            "singer": self.singer,
            "song_title": self.song_title,
            "watermark": self.watermark
        }

        self.size = size # 海报大小
        if(bg_image != None and isinstance(bg_image,Image.Image)):
            self.bg_image = bg_image
        elif(isinstance(bg_image, str)) :
            self.bg_image = Image.open(bg_image)
        else:
            self.bg_image = Image.new('RGBA', self.size, color=(0, 0, 0, 0))

        if(cover_image != None and isinstance(cover_image,Image.Image)):
            self.cover_image = cover_image
        elif(isinstance(cover_image, str)) :
            self.cover_image = Image.open(cover_image)
        else:
            self.cover_image = Image.new('RGBA', self.size, color=(0, 0, 0, 0))
        
        self.images_dict = {
            "bg_image": self.bg_image,
            "cover_image": self.cover_image
        }

    # 新建图片结构
    def new_pic(self, img_name, size, color, img=None):
        """
        新建图片结构\n
        img_name: 图片名\n
        size: 图片大小\n
        color: 图片颜色\n
        img: 图片\n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        if(img != None):
            self.images_dict[img_name] = img
        else:
            self.images_dict[img_name] = Image.new('RGBA', size, color=color)

    # 新建文字结构
    def new_text(self, text_name, text):
        """
        新建文字结构\n
        text_name: 文字名\n
        text: 文字\n
        ————————————————————————————————————————\n
        直接操作text_dict中的文字,无返回值\n
        """
        self.text_dict[text_name] = text

    # 重设图片颜色
    def recolor(self, img_name, new_color):
        """
        重设图片颜色\n
        img_name: 包含有images_dict中的key的列表\n
        new_color: 新的颜色\n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        for key, img in self.images_dict.items():
            if key in img_name:
                self.images_dict[key] = img.convert("RGBA")
                data = self.images_dict[key].getdata()
                newData = []
                for item in data:
                    if item[0] == 255 and item[1] == 255 and item[2] == 255:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(new_color)
                self.images_dict[key].putdata(newData)

    # 重设图片大小
    def resize(self, img_name,new_size):
        """
        重设图片大小\n
        img_name: 包含有images_dict中的key的列表\n
        new_size: 新的尺寸\n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        for key, img in self.images_dict.items():
            if key in img_name:
                self.images_dict[key] = img.resize(new_size, Image.ANTIALIAS)
        
    # 生成文字图像
    def text(self, font, font_color, spacing):
        """
        根据对象创建时传入的文本生成对应的图像\n
        font: 字体,传入时应为经由ImageFont.truetype()打开的实例\n
        font_color: 一个包含有lyrics, singer, song_tiyle键名的字典,键值为颜色\n
        spacing: 行间距\n
        ————————————————————————————————————————\n
        直接在images_dict中加入图片,无返回值\n
        """
        for key, text in self.text_dict.items():
            lines = text.splitlines()
            widths, heights = zip(*[font[key].getsize(line) for line in lines])
            size = (max(widths), sum(heights) + (len(lines) - 1) * spacing)
            image = Image.new('RGBA', size, color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(image)  
            draw.text((0, 0), text, fill=font_color[key], font=font[key])
            self.images_dict[key] = image

    # 对指定图像进行圆角处理
    def round(self, ronud_image):
        """
        对指定图像进行圆角处理\n
        ronud_image:一个键名为图像,键值为圆角度数的字典 \n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        for img, radius_value in ronud_image.items():
            # 如果img不是RGBA格式,则转换为RGBA格式
            if(self.images_dict[img].mode != "RGBA"):
                self.images_dict[img] = self.images_dict[img].convert("RGBA")
            trsp = self.images_dict[img].getchannel('A')
            trsp = trsp.getcolors()[0][1]
            alpha = Image.new('L', self.images_dict[img].size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.rounded_rectangle([0, 0, *self.images_dict[img].size], radius=radius_value, fill=trsp)
            self.images_dict[img].putalpha(alpha)
    
    # 对指定图像进行高斯模糊
    def blur(self, blur_image):
        """
        对指定图像进行高斯模糊\n
        blur_image:一个键名为图像,键值为模糊度的字典 \n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        for img, blur_value in blur_image.items():
            self.images_dict[img] = self.images_dict[img].filter(ImageFilter.GaussianBlur(blur_value))

    # 粘合图片
    def combine(self,pos):
        """
        粘合pos字典中键值对应的图片,粘合的顺序由字典的顺序决定,粘合后的图片存储在images_dict['poster']中\n
        pos: 一个键名为图像,键值为位置的字典 \n
        ————————————————————————————————————————\n
        直接操作images_dict中的图片,无返回值\n
        """
        self.images_dict['poster'] = Image.new('RGBA', self.size, color=(0, 0, 0, 0))
        for img, pos_s in pos.items():
            self.images_dict['poster'].paste(self.images_dict[img], pos_s, self.images_dict[img])