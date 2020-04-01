from wordcloud import WordCloud
# 加载内容
text = open('test.txt').read()
# 生成词云图片
wordcloud = WordCloud().generate(text)
# 展示生成的图片
image = wordcloud.to_image()
image.show()
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()