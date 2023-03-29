# 歌词海报生成器 (Lyrics Poster Generator)

歌词海报生成器是一个基于Python的脚本,可以生成一张简单的歌词海报

## 项目介绍

歌词海报生成器使用Python编写，借助PIL生成一张简单的歌词海报。歌词海报生成器可以指定背景图片、歌曲标题、歌词内容和字体。


## 主要功能

生成一张如下的歌词海报![图片](poster.png)

## 依赖

- Python 3.x
- Pillow (PIL Fork)

安装依赖：
 ` pip install pillow `

## 使用方法
- 将代码利用git或github的Code Download功能下载到本地
- 准备一个图片文件作为背景（例如：jay.jpg）
- 修改代码中的以下部分，以指定输入路径、输出路径、标题、歌词和字体路径
```
input_path = 'lib\jay.jpg'  
out_path = 'poster.png'  
song_title = '断了的弦'  
song_lyrics = '''歌词内容'''  
font_pth = '' #若不指定则默认使用中易黑体
```
- 运行代码：` python lyrics_poster.py `
- 查看生成的海报（例如：poster.png）  

## TODO
- 添加web界面
- 支持网络搜索歌词、专辑
- 更多样式的海报

