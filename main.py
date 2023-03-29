from PIL import Image, ImageDraw, ImageFont, ImageFilter
#输入路径
input_path = 'bli\jay.jpg'
#输出路径
out_path = 'poster.png'
#标题
song_title = '断了的弦'
#歌词
song_lyrics = '''
我突然释怀的笑
笑声盘旋半山腰
随风在飘摇啊摇
来到你的面前绕
你泪水往下的掉
说会记住我的好'''
#字体路径
font_pth = ''

class Picture():
    def __init__(self,pth = None,width=1080, height=1080):
        self.width = width
        self.height = height
        self.size = (width, height)
        if(pth != None):
            self.image = Image.open(pth)
        else:
            self.image = None
    
    '''
    对图片进行缩放处理
        size:缩放后的尺寸,若不指定则使用默认尺寸
    '''
    def ReSize(self,size = None):
        if(size == None):
            self.image = self.image.resize(self.size, Image.ANTIALIAS)
        else:
            self.image = self.image.resize(size, Image.ANTIALIAS)

    '''
    对图片进行高斯模糊处理
        num:高斯模糊参数,默认为60
    '''
    def GaussianBlur(self,num = 60):    
        self.image = self.image.filter(ImageFilter.GaussianBlur(num))

    '''
    对图片进行圆角处理
        radius:圆角半径,默认为30
        trsp:透明度,默认为255
    '''
    def Rounded(self, radius = 30, trsp = 255):
        self.image = self.image.convert('RGBA')
        alpha = Image.new('L', self.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.rounded_rectangle([0, 0, self.size[0], self.size[1]], radius=radius, fill=trsp)
        self.image.putalpha(alpha)

    '''
    产生一个纯色的图片
        color:颜色,默认为(180, 180, 180,0)
    '''
    def ColorBlock(self, color=(180, 180, 180,0)):
        colorblock = Image.new('RGBA', self.size, color)
        self.image = colorblock

    '''
        将图片对象返回
    '''
    def build(self):
        return self.image
    
class Writing():
    def __init__(self,txt,size,pos,font_pth = '',anchor = 'mm',color = (0,0,0)):
        if(font_pth != ''):
            self.font = ImageFont.truetype(font_pth,size)
        else:
            self.font = ImageFont.truetype('C:\Windows\Fonts\simhei.ttf',size)
        self.color = color
        self.txt = txt
        if(pos == None):
            pos = None
            # 自动计算文字位置//待完成
        else:
            self.pos = pos
        self.anchor = anchor
        self.draw = None
        self.image = None
    
    '''
    加载图片对象
        img:图片对象
    '''
    def load(self,imgObject):
        self.draw = ImageDraw.Draw(imgObject.image)

    '''
    为图片添加文字
        文字的属性,内容 在Writing类的初始化时指定
    '''
    def build(self):
        self.image = self.draw.text(self.pos, self.txt, font=self.font, fill=self.color,spacing=10,anchor=self.anchor)
        
class Content():
    def __init__(self,ac,bg,ac_shadow,bg_shadow,ac_pos,bg_pos):
        self.ac = ac.image #专辑封面
        self.bg = bg.image #局部背景(经过Writing类处理的)
        self.ac_shadow = ac_shadow.image #专辑封面阴影
        self.bg_shadow = bg_shadow.image #局部背景阴影
        self.ac_pos = ac_pos #专辑封面位置
        self.bg_pos = bg_pos #局部背景位置
        self.ac_shadow_pos = (ac_pos[0]+5,ac_pos[1]+5) #专辑封面阴影位置
        self.bg_shadow_pos = (bg_pos[0]+5,bg_pos[1]+5) #局部背景阴影位置
        self.image = None
    
    '''
    为海报生成内容对象
    '''
    def build(self):
        self.image = Image.new('RGBA', (self.bg.width+100,self.bg.height+100), (255, 255, 255, 0))
        self.image.paste(self.bg_shadow,self.bg_shadow_pos,self.bg_shadow)
        self.image.paste(self.bg,self.bg_pos,self.bg)
        self.image.paste(self.ac_shadow,self.ac_shadow_pos,self.ac_shadow)
        self.image.paste(self.ac,self.ac_pos,self.ac)
        return self.image

class Poster():
    def __init__(self,bg,con,pos = None):
        self.BG = bg
        self.Content = con
        if(pos == None):    
            self.pos =  (((self.BG.width)-(self.Content.bg.width))//2,((self.BG.height)-(self.Content.bg.height))//2)
        else:
            self.pos = pos
        self.image = None

    def build(self,pth='poster.png'):
        poster = Image.new('RGBA', (self.BG.width,self.BG.height))
        poster.paste(self.BG.image)
        poster.paste(self.Content.image,self.pos,self.Content.image)
        poster.save(pth, 'PNG')
        self.image = poster
        return poster

if __name__ == '__main__':
    overall_bg = Picture(input_path)
    overall_bg.ReSize()
    overall_bg.GaussianBlur()

    ac = Picture(input_path,width= 360,height= 360)
    ac.ReSize()
    ac.Rounded(radius = 50)

    local_bg = Picture(None,width= 860,height= 430)
    local_bg.ColorBlock(color=(255, 255, 255,0))
    local_bg.Rounded(trsp = 180)

    ac_shadow = Picture(None,ac.width,ac.height)
    ac_shadow.ColorBlock(color=(80, 80, 80, 255))
    ac_shadow.Rounded(trsp = 40,radius = 50)

    local_bg_shadow = Picture(None,local_bg.width,local_bg.height)
    local_bg_shadow.ColorBlock(color=(80, 80, 80, 255))
    local_bg_shadow.Rounded(trsp = 120)

    title = Writing(txt=song_title,
                size=50,
                pos=(630,107.5))
    title.load(local_bg)
    title.build()
    local_bg.build()

    lyrics = Writing(
        txt=song_lyrics,
        font_pth=font_pth,
        size=30,
        pos=(630,268.75))
    lyrics.load(local_bg)
    lyrics.build()

    con = Content(ac,local_bg,ac_shadow,local_bg_shadow,(20,35),(0,0))
    con.build()

    poster = Poster(overall_bg,con)
    poster.build()