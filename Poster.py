from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Picture():
    """
        图像类

        对图像进行处理,包括模糊,圆角,缩放

        图像具有 图片, 大小, 圆角半径, 模糊数值 属性,
        其中大小可有两种输入方式, 一种是直接输入宽高, 另一种是输入一个元组,
        输入元组时,元组的优先级高于宽高,
        宽高默认为1080,
        颜色默认为黑色(当输入图片对象为空时,会创建一个纯色图片),
        圆角半径默认为30,
        模糊数值默认为50.
    """
    def __init__(self,img=None,size=(0,0),width=1080,height=1080,color=(0,0,0,255),radius=30,blur=50):
        if(img != None):
            self.image = img
            self.image = self.image.convert('RGBA')
        else:
            self.image = Image.new('RGBA', (width,height), color)

        if(width != 0 or height != 0 and size == (0,0)):
            self.size = (width,height)
        else:
            self.size = size
        
        self.radius = radius
        self.blur = blur

    def resize(self,size=(0,0)):
        """
            缩放图片
            可以输入一个元组, 也可以不输入, 不输入时, 会使用初始化时的宽高
        """
        if(size == (0,0)):
            self.image = self.image.resize(self.size, Image.ANTIALIAS)
        else:
            self.image = self.image.resize(size, Image.ANTIALIAS)
            self.size = size
    
    def gaussianblur(self,blur=None):
        """
            模糊图片
            可以输入一个数值, 也可以不输入, 不输入时, 会使用初始化时的模糊数值
        """
        if(blur == None):
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.blur))
        else:
            self.image = self.image.filter(ImageFilter.GaussianBlur(blur))
            self.blur = blur

    def round(self,radius=None):
        """
            圆角图片
            可以输入一个数值, 也可以不输入, 不输入时, 会使用初始化时的圆角半径
        """
        trsp = self.image.getchannel('A')
        trsp = trsp.getcolors()[0][1]
        alpha = Image.new('L', self.size, 0)
        draw = ImageDraw.Draw(alpha)
        if(radius == None):
            draw.rounded_rectangle([0, 0, self.size[0], self.size[1]], radius=self.radius, fill=trsp)
        else:
            draw.rounded_rectangle([0, 0, self.size[0], self.size[1]], radius=radius, fill=trsp)
            self.radius = radius
        self.image.putalpha(alpha)

class Writing():
    """
        文字类

        创建透明背景的文字图片

        文字具有 文本, 颜色, 字体大小, 字体, 行间距 属性,
        其中文本为必须属性,
        颜色默认为白色,
        字体大小默认为30,
        字体默认为系统字体,
        行间距默认为5.
    """
    def __init__(self,text,color=(255,255,255,255),font_size=30,font = 'lib\msyh.ttc',spacing = 5):
        self.text = text
        self.font = ImageFont.truetype(font, font_size)
        self.color = color
        self.spacing = spacing
        self.size = None
        self.image = self.__initimg()
        
    def __initimg(self):
        """
            初始化图片

            会自动计算输入的文本的宽度和高度,并创建一张透明背景的图片
        """
        lines = self.text.splitlines()
        line_widths = [self.font.getsize(line)[0] for line in lines]
        line_heights = [self.font.getsize(line)[1] for line in lines]
        img_width = max(line_widths)
        img_height = sum(line_heights) + (len(lines) - 1) * self.spacing  # spacing 为行间距
        self.size = (img_width,img_height)
        return Image.new('RGBA', (img_width, img_height), color=(255, 255, 255,0))
    
    def draw(self):
        """
            绘制文字
        """
        draw = ImageDraw.Draw(self.image)
        draw.text((0, 0), self.text, fill=self.color, font=self.font)
        self.image.save("output.png","PNG")
        
class Combine():
    """
        合成类

        将两张图片合成为一张图片,图片2位于图片1的上层

        合成类具有 图片1, 图片2, 位置, 拓展 属性,
        前三种属性都为必须属性,拓展为可选属性,
        拓展是指合成后的图片向xy轴拓展的像素数,
        位置为元组, 元组的第一个值为x轴的偏移量, 第二个值为y轴的偏移量.
    """
    def __init__(self,img1,img2,pos,expand=0):
        self.img1 = img1.image
        self.img2 = img2.image
        self.size = (max(img1.size[0], img2.size[0]), max(img1.size[1], img2.size[1]))
        self.pos = pos
        self.image = self.__initimg(expand)
    
    def __initimg(self,expand=0):
        return Image.new('RGBA', (self.size[0]+expand,self.size[1]+expand), color=(255, 255, 255,0))
    
    def addimg(self,img,pos):
        self.image.paste(img.image,pos,img.image)
        
    def combine(self):
        self.image.paste(self.img1,(0,0,self.size[0],self.size[1]),self.img1)
        self.image.paste(self.img2,self.pos,self.img2)