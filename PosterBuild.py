from PIL import Image, UnidentifiedImageError
from Poster import Picture, Writing, Combine

text1 = '想要有直升机\n想要和你飞到宇宙去\n想要和你融化在一起\n融化在银河里' # 歌词
text2 = 'Jay Chou' # 歌手
text3 = '可爱女人' # 歌曲名
text4 = '@AlexHoshina' # 水印

def load_img(img_path):
    try:
        img = Image.open(img_path)
    except UnidentifiedImageError:
        print('读取失败,图片可能已损坏')
        return None
    except FileNotFoundError:
        print('文件不存在')
        return None
    except PermissionError:
        print('没有读取文件的权限')
        return None
    except Exception as e:
        print(f'发生了未知错误: {e}')
        return None
    return img

def style1(lyrcs, singer, song_title, watermark):
    img_path1 = "lib\\jay.jpg"
    img_path2 = "lib\\jay.jpg"
    img1 = load_img(img_path1)
    img2 = load_img(img_path2)

    #背景
    background = Picture(img=img1)
    background.resize((1080, 1080))
    background.gaussianblur(60)
    #

    #专辑封面
    album_cover = Picture(img=img2)
    album_cover.resize((300, 300))
    album_cover.round(30)
    #

    #专辑封面阴影
    album_cover_shadow = Picture(color=(0,0,0,20))
    album_cover_shadow.resize(album_cover.size)
    album_cover_shadow.round(album_cover.radius)
    #

    #歌词背景
    lyrcs_background = Picture(color=(180,180,180,80))
    lyrcs_background.resize((860,430))
    lyrcs_background.round(30)
    #

    #歌词背景阴影
    lyrcs_background_shadow = Picture(color=(0,0,0,20))
    lyrcs_background_shadow.resize(lyrcs_background.size)
    lyrcs_background_shadow.round(lyrcs_background.radius)
    #

    #计算各组件位置
    background_pos = (0,0)
    lyrcs_background_pos = ((background.size[0]-lyrcs_background.size[0])//2,((background.size[1]-lyrcs_background.size[1])//2))
    lyrcs_background_shadow_pos = (lyrcs_background_pos[0]+5,lyrcs_background_pos[1]+5)
    album_cover_pos = (lyrcs_background_pos[0]+((lyrcs_background_pos[1]+((lyrcs_background.size[1]-album_cover.size[1])//2))-lyrcs_background_pos[1]),(lyrcs_background_pos[1]+((lyrcs_background.size[1]-album_cover.size[1])//2)))
    album_cover_shadow_pos = (album_cover_pos[0]+5,album_cover_pos[1]+5)
    song_title_pos = (((lyrcs_background.size[0]-(album_cover.size[0]+album_cover_pos[0]-lyrcs_background_pos[0])-song_title.size[0])//2)+album_cover_pos[0]+album_cover.size[0],lyrcs_background_pos[1]+30)
    singer_pos = (album_cover_pos[0]+(album_cover.size[0]-singer.size[0])//2,album_cover_pos[1]+album_cover.size[1]+10)
    lyrcs_pos = (((lyrcs_background.size[0]-(album_cover.size[0]+album_cover_pos[0]-lyrcs_background_pos[0])-lyrcs.size[0])//2)+album_cover_pos[0]+album_cover.size[0],song_title_pos[1]+song_title.size[1]+30)
    watermark_pos = (background.size[0]-watermark.size[0]-10,background.size[1]-watermark.size[1]-10)
    #

    #将各组件合并
    poster = Combine(background, lyrcs_background_shadow,lyrcs_background_shadow_pos)
    poster.combine()
    poster.addimg(lyrcs_background, lyrcs_background_pos)
    poster.addimg(album_cover_shadow, album_cover_shadow_pos)
    poster.addimg(album_cover, album_cover_pos)
    poster.addimg(song_title, song_title_pos)
    poster.addimg(singer, singer_pos)
    poster.addimg(lyrcs, lyrcs_pos)
    poster.addimg(watermark, watermark_pos)
    #

    # 返回合并完成后的海报
    return poster.image


def main():
    # --------------------------------------------------------
    lyrcs = Writing(text=text1, font_size=40, color=(255, 255, 255, 255))#11x7
    lyrcs.draw()

    singer = Writing(text=text2, font_size=30, color=(255, 255, 255, 255))
    singer.draw()

    song_title = Writing(text=text3, font_size=50, color=(255, 255, 255, 255))
    song_title.draw()

    watermark = Writing(text=text4, font_size=20, color=(255, 255, 255, 80))
    watermark.draw()
    # ----------------------------------------------------------

    img = style1(lyrcs, singer, song_title, watermark)
    img.save('Poster.png','PNG')

if __name__ == '__main__':
    main()