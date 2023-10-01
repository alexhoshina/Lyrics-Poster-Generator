class Element():
    def __init__(self, name ,size):
        self.name = name
        self.size = size
        self.anchor = self.__initAnchor()
        self.pos_s = self.__initPos()
    def __initAnchor(self):
        return {
            "top": (int(self.size[0]/2), 0),
            "bottom": (int(self.size[0]/2), self.size[1]),
            "left": (0, int(self.size[1]/2)),
            "right": (self.size[0], int(self.size[1]/2)),
            "center": (int(self.size[0]/2), int(self.size[1]/2))
        }
    def __initPos(self):
        return {
            "pos":(0, 0),
            "top_pos": (int(self.size[0]/2), 0),
            "bottom_pos": (int(self.size[0]/2), self.size[1]),
            "left_pos": (0, int(self.size[1]/2)),
            "right_pos": (self.size[0], int(self.size[1]/2)),
            "center_pos": (int(self.size[0]/2), int(self.size[1]/2))
        }
    
    def setPos(self, **kwargs):
        if len(kwargs) != 1:
            raise ValueError("仅能以一个点作为移动点")
        pos_key, new_pos = list(kwargs.items())[0]
        if pos_key not in self.pos_s:
            raise ValueError(f"无效的点: {pos_key}")
        if pos_key == "pos":
            dx = new_pos[0] - self.pos_s["pos"][0]
            dy = new_pos[1] - self.pos_s["pos"][1]
        else:
            anchor_key = pos_key.replace("_pos", "")
            if anchor_key in self.anchor:
                dx = new_pos[0] - self.anchor[anchor_key][0]
                dy = new_pos[1] - self.anchor[anchor_key][1]
            else:
                raise ValueError(f"无效的点: {anchor_key}")
        # 使用偏移量来更新所有位置。
        for key in self.pos_s:
            self.pos_s[key] = (self.pos_s[key][0] + dx, self.pos_s[key][1] + dy)
        # 更新锚点位置。
        for key in self.anchor:
            self.anchor[key] = (self.anchor[key][0] + dx, self.anchor[key][1] + dy)


        

class Layout():
    def __init__(self, name, size, img_dict):
        self.name = name
        self.size = size
        self.anchor = self.__anchor()
        self.element_dict = self.__initElementDict(img_dict)

    def __str__(self):
        pos_dict = {}
        for e in self.element_dict.values():
            pos_dict[e.name] = e.pos_s["pos"]
        return str(pos_dict)

    def __anchor(self):
        return {
            "top": (int(self.size[0]/2), 0),
            "bottom": (int(self.size[0]/2), self.size[1]),
            "left": (0, int(self.size[1]/2)),
            "right": (self.size[0], int(self.size[1]/2)),
            "center": (int(self.size[0]/2), int(self.size[1]/2))
        }

    def __initElementDict(self, img_dict):
        element_dict = {}
        for key, img in img_dict.items():
            try:
                element_dict[key] = Element(key, img.size)
            # 捕获AttributeError异常
            except AttributeError:
                element_dict[key] = Element(key, img)
        return element_dict
    
    def place(self, **kwargs):# {"e_name":x,e_anchor:y,ee_name:xx,ee_anchor:yy,space:5}
        if(len(kwargs) < 2):
            raise ValueError("至少需要两个元素。")
        elif(len(kwargs) == 2):
            pass
        elif(len(kwargs) == 3):
            pass
        elif(len(kwargs) == 4):
            pass
        elif(len(kwargs) == 5):
            mark = kwargs.get('mark')
            mark_anchor = kwargs.get('mark_anchor')
            absolute = kwargs.get('absolute')
            absolute_anchor = kwargs.get('absolute_anchor')
            space = kwargs.get('space', (0, 0))
            
            if mark == "layout":
                mark_anchor_pos = self.anchor[mark_anchor]
            else:
                mark_anchor_pos = self.element_dict[mark].anchor[mark_anchor]

            absolute_anchor_pos = self.element_dict[absolute].anchor[absolute_anchor]

            new_anchor_pos_x = mark_anchor_pos[0] + space[0]
            new_anchor_pos_y = mark_anchor_pos[1] + space[1]

            dx = new_anchor_pos_x - absolute_anchor_pos[0]
            dy = new_anchor_pos_y - absolute_anchor_pos[1]
            new_pos_x = self.element_dict[absolute].pos_s["pos"][0] + dx
            new_pos_y = self.element_dict[absolute].pos_s["pos"][1] + dy

            self.element_dict[absolute].setPos(pos=(new_pos_x, new_pos_y))
        else:
            raise ValueError("最多只能有五个元素。")
        
    def getPos(self, element_name = ''):
        pos_dict = {}
        for e in self.element_dict.values():
            pos_dict[e.name] = e.pos_s["pos"]
        return pos_dict
            