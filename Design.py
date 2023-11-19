"""
布局控制类
"""
class Layout():
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.anchor = self.__setAnchor()
        self.link = []
        self.data = []

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

    def __updateAnchor(self, image):
        half_width, half_height = int(image.size[0] / 2), int(image.size[1] / 2)
        anchor = {
            "top_left" : image.position,
            "top" : (image.position[0] + half_width, image.position[1]),
            "top_right" : (image.position[0] + image.size[0], image.position[1]),
            "left" : (image.position[0], image.position[1] + half_height),
            "center" : (image.position[0] + half_width, image.position[1] + half_height),
            "right" : (image.position[0] + image.size[0], image.position[1] + half_height),
            "bottom_left" : (image.position[0], image.position[1] + image.size[1]),
            "bottom" : (image.position[0] + half_width, image.position[1] + image.size[1]), 
            "bottom_right" : (image.position[0] + image.size[0], image.position[1] + image.size[1])
        }
        return anchor

    def __update(self, image, dx, dy):
        image.position = (image.position[0] + dx, image.position[1] + dy)
        image.anchor = self.__updateAnchor(image)
        if image.link:
            for image0 in image.link:
                self.__update(image0, dx, dy)
    
    def add(self, image1, anchor1, image2, anchor2, dxdy):
        dx = image1.anchor[anchor1][0] - image2.anchor[anchor2][0] + dxdy[0]
        dy = image1.anchor[anchor1][1] - image2.anchor[anchor2][1] + dxdy[1]
        image1.link.append(image2)
        self.data.append( {
            "image1" : 'self.' + image1.name,
            "anchor1" : anchor1,
            "image2" : 'self.' + image2.name,
            "anchor2" : anchor2,
            "dxdy" : dxdy
        } )
        self.__update(image2, dx, dy)

    def __str__(self):
        return str(self.data)