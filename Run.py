import sys,os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtGui import QPixmap
from lxml import etree
from requests import get as requests_get
from PIL import Image
from numpy import array as nparray
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QFileDialog, QMessageBox
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import wordcloud
import jieba.analyse
import snownlp
from TLM import Ui_MainWindow
from weibo_spider_comments_mysql import create_table,get_url_data
from cut_words import get_data, keywords


cookie = {"Cookie":""}
url = ""

#Function

def FindID(string):
    start1 = 'uid='
    end1 = '&rl='
    # 使用find找到开始截取的位置
    s = string.find(start1)
    # 只要s不等于-1，说明找到了http
    while s != -1:
        # 找结束位置
        e = string.find(end1, s)
        # 截取字符串 结束位置=结束字符串的开始位置+结束字符串的长度
        sub_str = string[s+len(start1):e]
        return sub_str
        # 找到下一个开始位置
        # 如果没有找到下一个开始的位置，相当于写了一句s=-1,while循环的条件不成立，结束循环

def word_cloud(self):
    plt.figure(num='fig1')
    lyric = ''
    f = open('./static/data_keywords.dat', 'r')

    for i in f:
        lyric += f.read()

    result = jieba.analyse.textrank(lyric, topK=50, withWeight=True)

    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]

    image = Image.open('./static/background.png')
    graph = nparray(image)
    wc = wordcloud.WordCloud(font_path='./static/msyh.ttc', background_color='White',
                   max_words=50, mask=graph)
    wc.generate_from_frequencies(keywords)
    image_color = wordcloud.ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.imshow(wc.recolor(color_func=image_color))
    plt.axis("off")
    self.canvas.draw()

def sentiment(self):
    plt.figure(num='fig2')
    comment = []
    pos_count = 0
    neg_count = 0
    for line_data in open("./static/data_keywords.dat"):
        comment = line_data
        s = snownlp.SnowNLP(comment)
        rates = s.sentiments
        if rates >= 0.6:
            pos_count += 1
        elif rates < 0.4:
            neg_count += 1
        else:
            pass
    labels = 'Positive Side', 'Negative Side'
    fracs = [pos_count, neg_count]
    explode = [0.1, 0]  # 0.1 凸出这部分，
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
    self.canvas2.draw()

class mwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mwindow, self).__init__()
        self.setupUi(self)
        self.figure = plt.figure(num='fig1')#不指明具体的num，则会覆盖前一个fig！！！！！！！！！花了老子一天的时间
        self.canvas = FigureCanvas(self.figure)

        self.figure2 = plt.figure(num='fig2')
        self.canvas2 = FigureCanvas(self.figure2)

    def btnUpload_clicked(self):
        global cookie,url
        cookie['Cookie'] = self.textCookie.toPlainText()
        url = self.textURL.toPlainText()
        QMessageBox.information(self,
                                    "提示",
                                    "上传OK！",
                                    QMessageBox.Yes)

    def btnWeibo_clicked(self):
        # if(cookie == "" or url == ""):
        #     QMessageBox.information(self,
        #                             "提示",
        #                             "脑子呢？",
        #                             QMessageBox.Yes)
        #     return
        # id = FindID(url)
        # create_table(id)
        # word_count = 1
        # base_url = url + '&page='
        # first_url = base_url + '1'  # LINSHAOBO
        # html = requests_get(first_url, cookies=cookie).content
        # selector = etree.HTML(html)
        #
        # repost_num = selector.xpath('body/div/span/a/text()')[0][3:-1]
        # self.tbSpread.setPlainText(repost_num)
        # comment_num = selector.xpath('//span[@class="pms"]/text()')[0][4:-2]
        # self.tbTopic.setPlainText(comment_num)
        # like_num = selector.xpath('body/div/span/a/text()')[1][2:-1]
        # self.tbLiked.setPlainText(like_num)
        #
        # controls = selector.xpath('//input[@name="mp"]')
        #
        # if controls:
        #     pageNum = int(controls[0].attrib['value'])
        # else:
        #     pageNum = 1
        #get_url_data(base_url, pageNum, word_count, id, cookie)

        #get_data(id)
        #keywords(self)

        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        word_cloud(self)
        self.gridlayout.addWidget(self.canvas,0,1)
        self.gridlayout = QGridLayout(self.groupBox_2)  # 继承容器groupBox
        sentiment(self)
        self.gridlayout.addWidget(self.canvas2,0,1)


    def btnBzhan_clicked(self):
        QMessageBox.information(self,
                                "提示",
                                "TLM狗东西！",
                                QMessageBox.Yes)

    def btnUploadPic_clicked(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;*.png;;All Files(*)")
        self.lblPic.setPixmap(QPixmap(imgName).scaled(self.lblPic.width(),self.lblPic.height()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mwindow()
    w.btnUpload.clicked.connect(w.btnUpload_clicked)
    w.btnWeibo.clicked.connect(w.btnWeibo_clicked)
    w.btnUploadPic.clicked.connect(w.btnUploadPic_clicked)
    w.btnBzhan.clicked.connect(w.btnBzhan_clicked)
    w.show()
    sys.exit(app.exec_())