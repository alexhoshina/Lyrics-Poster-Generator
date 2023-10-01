from Poster import Poster
from Design import Layout
from PIL import Image, ImageFont

def style1():

    poster_size = (1200, 2000)

    #--------------text----------------
    song_title = "可爱女人"
    singer = "Jay Chou"
    lyrics = """
    漂亮的让我面红的 可爱女人
    温柔的让我心疼的 可爱女人
    透明的让我感动的 可爱女人
    坏坏的让我疯狂的 可爱女人
    漂亮的让我面红的 可爱女人
    温柔的让我心疼的 可爱女人
    透明的让我感动的 可爱女人
    坏坏的让我疯狂的 可爱女人
            """
    watermark = "kagurahoshina"
    spacing = 5

    font = {
        'song_title':ImageFont.truetype("C\\Windows\\Fonts\\msyh.ttc", 70),
        'singer':ImageFont.truetype("C\\Windows\\Fonts\\msyh.ttc", 40),
        'lyrics':ImageFont.truetype("C\\Windows\\Fonts\\msyh.ttc", 45),
        'watermark':ImageFont.truetype("C\\Windows\\Fonts\\msyh.ttc", 20)
    }
    font_color = {
        "lyrics": (255, 255, 25, 255),
        "singer": (255, 25, 255, 255),
        "song_title": (0, 255, 255, 255),
        "watermark": (255, 0, 0, 255)
    }
    #----------------------------------

    #--------------img-----------------
    bg_img_path = "lib\jay.jpg"
    bg_img_size = (1080, 1920)
    bg_img = Image.open(bg_img_path)

    cover_img_path = "lib\jay.jpg"
    cover_img_size = (400, 400)
    cover_img = Image.open(cover_img_path)
    #----------------------------------

    poster = Poster(lyrics, singer, song_title, bg_img, cover_img, watermark, poster_size)
    
    poster.resize(["bg_image"], bg_img_size)
    poster.resize(["cover_image"], cover_img_size)

    poster.text(font, font_color, spacing)

    poster.blur({"bg_image":200})

    poster.round({"bg_image":30, "cover_image":50})

    #-----------布局设计----------------
    layout = Layout("test1", poster_size, poster.images_dict)
    layout.place(mark='layout',mark_anchor='center',absolute='bg_image',absolute_anchor='center',space=(0, 0))
    layout.place(mark='bg_image',mark_anchor='top',absolute='cover_image',absolute_anchor='top',space=(-int(100+(cover_img_size[0]/2)), 50))
    layout.place(mark='cover_image',mark_anchor='right',absolute='song_title',absolute_anchor='left',space=(200, 0))
    layout.place(mark='song_title',mark_anchor='bottom',absolute='singer',absolute_anchor='top',space=(0, 50))
    layout.place(mark='bg_image',mark_anchor='center',absolute='lyrics',absolute_anchor='center',space=(0, 0))
    layout.place(mark='bg_image',mark_anchor='bottom',absolute='watermark',absolute_anchor='bottom',space=(0, 0))
    #----------------------------------

    
    pos = layout.getPos()

    poster.combine(pos)

    poster.images_dict['poster'].show()
    

if __name__ == "__main__":
    style1()
    