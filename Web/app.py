from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, UnidentifiedImageError
from Poster import Picture, Writing, Combine
import os
app = Flask(__name__)

song_title = " "
singer = " "
lyrics = " "


if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/save_txt', methods=['POST'])
def save_txt():
    song_title = request.form.get("song_title")
    singer = request.form.get("singer")
    lyrics = request.form.get("lyrics")
    build_poster(lyrics, singer, song_title, "@AlexHoshina")
    # 在此处理数据
    print(song_title, singer, lyrics)
    
    return jsonify({"status": "success", "message": "海报已保存"})

@app.route('/upload_bg', methods=['POST'])
def upload_bg():
    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1]
    custom_name = f"bg{file_ext}"
    file.save(os.path.join('uploads', custom_name))
    build_poster(lyrics, singer, song_title, "@AlexHoshina")
    return "File uploaded and saved."

@app.route('/upload_cover', methods=['POST'])
def upload_cover():
    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1]
    custom_name = f"cover{file_ext}"
    file.save(os.path.join('uploads', custom_name))
    build_poster(lyrics, singer, song_title, "@AlexHoshina")
    return "File uploaded and saved."

@app.route('/upload_font', methods=['POST'])
def upload_font():
    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1]
    custom_name = f"font{file_ext}"
    file.save(os.path.join('uploads', custom_name))
    build_poster(lyrics, singer, song_title, "@AlexHoshina")
    return "File uploaded and saved."

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/preview_image')
def preview_image():
    # 如果图片文件名是固定的，可以直接在此处指定
    image_file = 'Poster.png'
    return send_from_directory('static', image_file)

def build_poster(text1, text2, text3, text4):
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
        img_path1 = "uploads\\bg.jpg"
        img_path2 = "uploads\\cover.jpg"
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
    # --------------------------------------------------------

    lyrcs = Writing(text=text1, font_size=40, color=(0, 0, 0, 255))#11x7
    lyrcs.draw()

    singer = Writing(text=text2, font_size=30, color=(0, 0, 0, 255))
    singer.draw()

    song_title = Writing(text=text3, font_size=50, color=(0, 0, 0, 255))
    song_title.draw()

    watermark = Writing(text=text4, font_size=20, color=(0, 0, 0, 80))
    watermark.draw()
    # ----------------------------------------------------------
    img = style1(lyrcs, singer, song_title, watermark)
    img.save('static/Poster.png','PNG')
    return img

if __name__ == '__main__':
    app.run(debug=True)
