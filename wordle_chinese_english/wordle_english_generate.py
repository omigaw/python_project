# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pylab

f_path = "D:\\yes-minister.txt"
with open(f_path) as f:
    text = f.read()
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
pylab.show()