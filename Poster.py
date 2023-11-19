from Picture import Picture
from Design import Layout
from Text import Text
import yaml
"""
海报类
"""
Air = (0, 0, 0, 0)
class Poster():
    def __init__(self, name, size, image_list):
        self.name = name

        self.poster = Picture(name, None, size, Air)
        self.layout = Layout('layout', size)

        if isinstance(image_list, list):
            self.image_list = self.__init_image_list(image_list)
        elif isinstance(image_list, dict):
            self.image_list = []
            self.__init_dict_image_list(image_list)

    def __getattr__(self, name):
        for n in self.image_list:
            if name == n.name:
                return n
        return getattr(self.poster, name)
    
    def __init_image_list(self, image_list):
        ok_list = []
        for image in image_list:
            if("image_path" in image.keys()):
                ok_list.append(Picture(**image))
            elif("text" in image.keys()):
                ok_list.append(Text(**image))
        return ok_list

    def __init_dict_image_list(self, d):
        l=[]
        for dict0 in d.values():
            for key in dict0:
                if isinstance(dict0[key], str):
                    if dict0[key].startswith('(') and dict0[key].endswith(')'):
                        dict0[key] = eval(dict0[key])
            l.append(dict0)
            
            if("image_path" in dict0.keys()):
                self.image_list.append(Picture(**dict0))
            elif("text" in dict0.keys()):
                self.image_list.append(Text(**dict0))
        
    def yaml_add(self, list):
        for dict in list:
            for key,value in dict.items():
                if((value not in self.anchor.keys()) and (not isinstance(value, tuple))):
                    dict[key] = eval(value)
            self.layout.add(**dict)

    def build(self, order = None):
        if order:
            self.image_list.sort(key=lambda x: order.index(x.name))
        for image in self.image_list:
            self.poster.paste(image, image.position, image)
            
    def printPosition(self):
        for image in self.image_list:
            print(image.name, image.position)

    def savecfg(self):
        element_data = {image.name: eval(image.__str__()) for image in self.image_list}
        layout_data = eval(self.layout.__str__())

        config_data = {
            'Element': element_data,
            'Layout': layout_data,
            'Order': [image.name for image in self.image_list]
        }

        yaml_path = f'{self.name}.yaml'
        with open(yaml_path, 'w', encoding='utf-8') as file:
            yaml.dump(config_data, file, encoding='utf-8')

        print(yaml.dump(config_data))