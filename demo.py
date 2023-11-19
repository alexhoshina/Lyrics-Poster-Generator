import yaml
from Poster import Poster

yaml_path = 'demo.yaml'

with open(yaml_path, 'r', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

poster = Poster("demo", (1200, 2000), cfg['Element'])
poster.yaml_add(cfg['Layout'])
poster.build(cfg['Order'])

poster.show()
poster.save('demo.png')