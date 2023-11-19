from PIL import Image, ImageFilter, ImageDraw
"""
图片类
"""
class Picture():
    def __init__(self, name, image_path, size = None, color = None, round = None, blur = None):
        self.flag = False

        self.name = name
        if image_path :
            self.image_path = image_path
            self.image = Image.open(image_path)
            if(self.image.mode != "RGBA"):
                self.image = self.image.convert("RGBA")
        elif (image_path == None):
            self.image_path = None
            self.color = color
            self.image = Image.new('RGBA', size, color)
        
        if size:
            if self.image.size != size:
                self.reSize(size)

        self.round_v = None
        self.blur_v = None

        if round:
            self.round(round)
        if blur:
            self.blur(blur)

        self.anchor = self.__setAnchor()
        self.position = self.anchor['top_left']
        self.link = []
        
        self.flag = True

    def __getattr__(self, name):
        return getattr(self.image, name)
    
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

    def __str__(self):
        dict = {}
        dict1 = {}
        dict['name'] = self.name
        dict['image_path'] = self.image_path
        dict['size'] = self.size
        if 'color' in self.__dict__.keys():
            dict['color'] = self.color
        if self.round_v != None:
            dict['round'] = self.round_v
        if self.blur_v != None:
            dict['blur'] = self.blur_v
        dict1[self.name] = dict
        return str(dict1)

    def reLoda(self, image_path):
        self.image = Image.open(image_path)
        if(self.image.mode != "RGBA"):
            self.image = self.image.convert("RGBA")
        if self.round_v != None:
            self.round(self.round_v)
        if self.blur_v != None:
            self.blur(self.blur_v)
        self.anchor = self.__setAnchor()
        
    def reSize(self, size, resample=Image.LANCZOS):
        self.image = self.image.resize(size, resample=resample)
        if self.flag and self.round_v != None:
            self.round(self.round_v)
        self.anchor = self.__setAnchor()

    def reColor(self, color):
        self.image = Image.new('RGBA', self.size, color=color)
        if self.round_v != None:
            self.round(self.round_v)
        if self.blur_v != None:
            self.blur(self.blur_v)
        
    def round(self, value):
        if(isinstance(value, int)):
            value = ['all', value]
        if(value[0] == 'all'):
            value[0] = ['top_left', 'top_right', 'bottom_left', 'bottom_right']

        anchors = value[0]

        image = self.image

        width, height = image.size
        mask = Image.new("L", (width, height), 0) 
        draw = ImageDraw.Draw(mask)

        draw.rectangle((0, 0, width, height), fill=255)

        corner_mapping = {
            "top_left": ((0, 0, value[1], value[1]), (0, 0, value[1]*2, value[1]*2), 180, 270),
            "top_right": ((width - value[1], 0, width, value[1]), (width - value[1]*2, 0, width, value[1]*2), 270, 0),
            "bottom_left": ((0, height - value[1], value[1], height), (0, height - value[1]*2, value[1]*2, height), 90, 180),
            "bottom_right": ((width - value[1], height - value[1], width, height), (width - value[1]*2, height - value[1]*2, width, height), 0, 90)
        }

        for corner, ((rx1, ry1, rx2, ry2), (px1, py1, px2, py2), start_angle, end_angle) in corner_mapping.items():
            if corner in anchors:
                draw.rectangle((rx1, ry1, rx2, ry2), fill=0)
                draw.pieslice((px1, py1, px2, py2), start_angle, end_angle, fill=255)

        self.image = Image.composite(image, Image.new("RGBA", self.size, (0, 0, 0, 0)), mask)
        self.round_v = value

    def blur(self, value):
        self.image = self.image.filter(ImageFilter.GaussianBlur(value))
        self.blur_v = value
        if self.round_v != None:
            self.round(self.round_v)

