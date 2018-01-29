# -*- coding: utf-8 -*-
import jieba
from PIL import Image
import numpy
from wordcloud import WordCloud,ImageColorGenerator
import pylab
import matplotlib.pyplot as plt

f_path = 'D:\\disney-wordle.txt'
with open(f_path) as f:
    text = f.read()
mytext = " ".join(jieba.cut(text))


# 图像处理
img = Image.open('mao.jpg')
graph = numpy.array(img)
wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\SIMLI.TTF",background_color='white',
                      max_words=8000,mask=graph,max_font_size=40,random_state=42).\
            generate(mytext)

image_colors=ImageColorGenerator(graph)
plt.imshow(wordcloud.recolor(color_func=image_colors))
plt.axis("off")
pylab.show()