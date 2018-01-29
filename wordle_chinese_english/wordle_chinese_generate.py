# -*- coding: utf-8 -*-
import jieba
import numpy
from PIL import Image
import jieba.analyse
from wordcloud import WordCloud,ImageColorGenerator
import pylab
import matplotlib.pyplot as plt

f_path = 'D:\\yes-minister-cn.txt'
with open(f_path) as f:
    text = f.read()
word_frequence = dict()
result = jieba.analyse.textrank(text,topK=80,withWeight=True)   # 分析单词出现频率
for i in result:
    word_frequence[i[0]]=i[1]
print(word_frequence)
del word_frequence['英国']
word_frequence['爱'] =1.0
print(word_frequence)
mytext = " ".join(jieba.cut(text))

# 图像处理
img = Image.open('mao.jpg')
graph = numpy.array(img)

wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\SIMLI.TTF",
                     background_color='black',max_words=80,
                     mask=graph).generate_from_frequencies(word_frequence)
# word_frequence 为字典形式即可
image_color = ImageColorGenerator(graph)
plt.imshow(wordcloud.recolor(color_func=image_color))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
pylab.show()
