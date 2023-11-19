from PIL import Image, ImageFont, ImageDraw
"""
文字类
"""
Air = (0, 0, 0, 0)
class Text():
    def __init__(self, name, text, font, font_size, font_color, spacing = 5):
        self.name = name
        self.text = text
        self.font_path = font
        self.font_size = font_size
        self.font = ImageFont.truetype(font, font_size, encoding="gb")
        
        self.spacing = spacing
        self.font_color = font_color
        
        self.image = Image.new('RGBA', self.__getSize(), color=Air)
        
        self.__drawText()

        self.anchor = self.__setAnchor()
        self.position = self.anchor['top_left']
        self.link = []

    def __getattr__(self, name):
        return getattr(self.image, name)

    def __getSize(self):
            lines = self.text.splitlines()
            widths, heights = zip(*[self.font.getsize(line) for line in lines])
            return (max(widths), sum(heights) + (len(lines) - 1) * self.spacing)
        
    def __setAnchor(self):
        size = self.size
        half_width, half_height = int(size[0] / 2), int(size[1] / 2)
        anchor = {
            "top_left": (0, 0),
            "top": (half_width, 0),
            "top_right": (size[0], 0),
            "left": (0, half_height),
            "center": (half_width, half_height),
            "right": (size[0], half_height),
            "bottom_left": (0, size[1]),
            "bottom": (half_width, size[1]),
            "bottom_right": (size[0], size[1])
        }
        return anchor

    def __drawText(self):
        draw = ImageDraw.Draw(self.image)  
        y_text = 0
        lines = self.text.splitlines()
        for line in lines:
            draw.text((0, y_text), line, fill=self.font_color, font=self.font)
            y_text += self.font.getsize(line)[1] + self.spacing

    def __str__(self):
        dict = {}
        dict1 = {}
        dict['name'] = self.name
        dict['text'] = self.text
        dict['font'] = self.font_path
        dict['font_size'] = self.font_size
        dict['font_color'] = self.font_color
        dict['spacing'] = self.spacing
        dict1[self.name] = dict
        return str(dict1)


    def reSize(self,font_size):
        self.font = ImageFont.truetype(self.font_path, font_size, encoding="gb")
        self.image = Image.new('RGBA', self.__getSize(), color=Air)
        self.__drawText()
        self.anchor = self.__setAnchor()

    def reText(self,text,font=None):
        if font:
            self.font = ImageFont.truetype(font, self.font.size, encoding="gb")
        self.text = text
        self.image = Image.new('RGBA', self.__getSize(), color=Air)
        self.__drawText()
        self.anchor = self.__setAnchor()

    def reColor(self,font_color):
        self.font_color = font_color
        self.image = Image.new('RGBA', self.__getSize(), color=Air)
        self.__drawText()
