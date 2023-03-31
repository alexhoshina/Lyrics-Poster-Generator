# 歌词海报生成器 (Lyrics Poster Generator)

歌词海报生成器是一个基于Python的脚本,可以生成一张简单的歌词海报

## 项目介绍

歌词海报生成器使用Python编写，借助PIL生成一张简单的歌词海报。歌词海报生成器可以指定背景图片、歌曲标题、歌词内容和字体。


## 主要功能

生成一张如下的歌词海报![图片](poster.png)

## 依赖

- Python 3.x
- Pillow

安装依赖：
 ` pip install pillow `

## 使用方法
- 将代码利用git或github的Code Download功能下载到本地
- 准备一个图片文件作为背景（例如：jay.jpg）
- 修改代码中的以下部分
```
text1 = '想要有直升机\n想要和你飞到宇宙去\n想要和你融化在一起\n融化在银河里' # 歌词
text2 = 'Jay Chou' # 歌手
text3 = '可爱女人' # 歌曲名
text4 = '@AlexHoshina' # 水印
```
- 运行代码：` python PosterBuild.py `
- 查看生成的海报（例如：poster.png）  

## TODO
- 添加web界面
- 支持网络搜索歌词、专辑
- 更多样式的海报

