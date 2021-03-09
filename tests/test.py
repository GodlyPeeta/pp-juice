'''import base64
import lzma
from ossapi import ossapi
token = 'token'
api = ossapi(token)

b = api.get_replay({'b': 1919312, 'u': 2094566, 'mods': 1112})
print(b)
str = b['content']
str2 =base64.b64decode(str)
f = open('./output/test.lzma', 'wb')
f.write(str2)
output = lzma.open('./output/test.lzma', 'rb')
data = output.read()
data=data.decode("utf-8")
arr = data.split(',')
out=[]
for i in arr:
    out.append(i.split('|'))
print(out)
f.write(str2)
'''
#from PIL import Image
'''im = Image.open("loadingbar.png")
rgb_im = im.convert('RGBA')
pixels = rgb_im.load()

for i in range(0, 24): 
    pixels[i, 0] = (0, 255, 0)

im.save("loading_grid.png")'''



'''from ossapi import ossapi
import config    
import datetime
from multiprocessing import Pool

token = config.OSU_TOKEN[0]
api = ossapi(token)
apis = []
for i in config.OSU_TOKEN:
    #print(i)
    apis.append(ossapi(i))
#print(apis)'''

'''a = datetime.datetime.now()

for i in range(5):
    #print("a")
    api.get_beatmaps({"b": 2640411, "limit": 1})[0]
    #print('b')

b = datetime.datetime.now()
print((a-b).total_seconds()*1000)'''














'''def temp(num):
    return api.get_beatmaps( {"b": 2640411, "limit": 1} )[0]

def double(i):
    #print("I'm process", getpid())
    return i * 2

a = datetime.datetime.now()
t = api.get_user_best({"u": "GodlyPeeta", "limit": 5})
#print("a")
t = []
for i in range(5):
    t.append()

#print(t)
if __name__ == '__main__':    
    with Pool() as pool:
        result = pool.map(temp, [1, 2, 3, 4, 5])
        print(result)
#print(len(beatmap))
#print('b')

b = datetime.datetime.now()
print((a-b).total_seconds()*1000)'''

'''from multiprocessing import Pool
from os import getpid



def double(i):
    print("I'm process", getpid())
    return i * 2

if __name__ == '__main__':
    print("a")
    with Pool() as pool:
        a = datetime.datetime.now()
        result = pool.map(double, [1, 2, 3, 4, 5])
        print(result)
        b = datetime.datetime.now()
        print((a-b).total_seconds()*1000)'''

'''import threading 

print("sdkjfksdf")

def temp(res):
    res.append( api.get_beatmaps( {"b": 2640411, "limit": 1} )[0] )

res = []

if __name__ == "__main__": 
    a = datetime.datetime.now()
    # creating thread 
    t1 = threading.Thread(target=temp, args=(res,)) 
    t2 = threading.Thread(target=temp, args=(res,)) 
    t3 = threading.Thread(target=temp, args=(res,)) 
    t4 = threading.Thread(target=temp, args=(res,)) 
    t5 = threading.Thread(target=temp, args=(res,)) 
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
    t3.start()
    t4.start()
    t5.start()
  
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
    t3.join()
    t4.join()
    t5.join()
    b = datetime.datetime.now()
    print((a-b).total_seconds()*1000)
    # both threads completely executed 
    print(res) '''

'''print(type([1,2])==list)'''

'''
import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(220, 32),
                QtWidgets.qApp.desktop().availableGeometry()
        ))

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec_()'''
'''from PIL import Image
string = '0.0313725 1.0000000 0.0000000 0.3764706 0.0235294 0.0156863 0.3176471 0.3372549 0.1490196 0.2549020 0.5294118 0.0274510 0.0000000 0.3019608 0.1529412 0.0392157 0.6117647 0.0901961 0.5490196 0.0078431 0.0235294 0.0156863 0.2549020 0.6666667 0.0196078 0.4313725 0.4117647 0.2862745 0.1411765 0.0392157 0.0313725 0.2823529 0.1568627 0.0156863 0.0156863 0.5568627 0.6862745 0.2078431 0.6666667 0.2313725 0.0000000 0.9803922 0.2392157 0.0156863 0.0117647 0.0039216 0.0000000 0.2000000 0.2156863 0.0352941 0.0392157 0.0352941 0.3137255 0.3372549 0.0392157 0.0156863 0.0039216 0.1960784 0.0156863 0.0078431 0.2509804 0.3058824 0.2470588 0.0392157 0.0352941 0.2196078 0.2862745 0.2784314 0.1529412 0.1372549 0.1333333 0.4392157 0.1921569 0.3294118 0.6784314 0.1607843 0.2627451 0.0078431 0.2078431 0.2313725 0.0196078 0.9843137 0.2941176 0.0235294 0.9568627 0.9450980 0.9058824 0.3215686 0.9686275 0.0156863 0.9607843 0.1450980 0.9411765 0.9176471 0.9058824 0.0000000 0.2235294 0.2274510 0.2862745 0.3529412 0.9568627 0.9333333 0.8980392 0.2196078 0.2352941 0.3803922 0.9372549 0.4000000 0.2745098 0.2784314 0.6745098 0.4039216 0.2392157 0.3176471 0.3450980 0.3490196 0.6627451 0.4980392 0.6352941 0.2117647 0.0235294 0.9764706 0.3411765 0.0078431 0.9764706 0.4196078 0.8509804 0.2941176 0.9607843 0.0313725 0.9490196 0.2313725 0.8980392 0.0235294 0.8941176 0.1568627 0.4431373 0.3568627 0.4941176 0.3450980 0.3254902 0.3058824 0.9176471 0.2156863 0.3294118 0.2862745 0.9764706 0.0039216 0.0274510 0.0156863 0.2313725 0.2352941 0.0235294 0.1921569 0.3921569 0.0235294 0.0039216 0.0352941 0.3764706 0.3607843 0.0117647 0.9490196 0.3176471 0.3215686 0.9176471 0.9058824 0.3098039 0.3647059 0.2862745 1.0000000 0.3294118 0.3960784 0.9568627 0.9725490 0.8627451 0.4823529 0.8941176 0.9058824 0.9137255 0.1450980 0.0196078 0.8549020 0.0000000 0.2196078 0.9176471 0.9019608 0.9254902 0.0313725 0.8784314 0.0078431 0.8745098 0.0392157 0.8705882 0.8862745 0.9607843 0.0352941 0.0392157 0.6431373 0.3098039 0.4705882 0.1803922 0.9803922 0.2784314 0.3960784 0.9372549 0.3294118 0.9254902 0.4156863 0.9372549 0.2705882 0.9647059 0.2823529 0.9686275 0.2862745 0.9647059 0.3137255 0.9568627 0.3098039 0.9882353 0.0078431 0.9176471 0.0000000 0.0352941 0.3098039 0.9686275 0.2941176 0.9098039 0.0313725 0.9176471 0.1960784 0.8980392 0.2470588 0.8588235 0.3764706 0.2274510 0.2431373 0.0117647 0.3098039 0.2156863 0.5764706 0.2980392 0.9725490 0.3686275 0.5294118 0.9568627 0.3686275 0.9019608 0.3921569 0.9333333 0.4352941 0.9529412 0.3254902 0.9372549 0.1607843 0.8901961 0.1568627 0.9411765 0.9725490 0.9568627 0.2313725 0.9529412 0.9098039 0.8901961 0.3607843 0.8901961 0.8823529 0.9529412 0.3411765 0.8823529 0.8862745 0.9450980 0.3725490 0.8823529 0.9764706 0.9725490 0.2196078 0.3372549 0.6431373 0.1490196 0.2352941 0.0039216 1.0000000 0.2431373 0.4313725 0.4431373 0.3960784 0.4901961 0.4549020 0.3647059 0.3686275 0.3058824 0.3098039 0.2666667 0.3882353 0.4274510 0.2823529 0.2823529 0.3686275 0.8862745 0.2549020 0.2352941 0.2392157 0.3725490 0.1294118 0.3215686 0.3333333 0.0352941 0.0039216 0.0000000 0.3215686 0.8901961 0.2549020 0.2745098 0.0352941 0.1333333 0.2745098 0.2196078 0.1450980 0.6235294 0.2392157 0.0078431 1.0000000 0.3882353 0.4980392 0.4823529 0.3882353 0.4666667 0.1254902 0.3333333 0.0078431 0.0156863 0.0196078 0.4509804 0.3607843 0.0392157 0.0078431 0.0274510 0.3333333 0.9450980 0.0235294 0.0313725 0.3215686 0.3333333 0.0000000 0.3137255 0.1921569 0.2784314 0.0352941 0.9411765 0.9686275 0.9411765 0.2823529 0.1686275 0.0039216 0.3647059 0.2627451 0.6666667 0.1333333 0.2274510 0.2156863'
print(len(string.split()))
arr=string.split()

im = Image.open('p6.png')
print(im.size[0])
print(im.size[1])
rgb_im = im.convert('RGBA')
pixels = rgb_im.load()
print(arr)

for i in range(0, 360): 
    #print(int(255*float(arr[i])))
    pixels[i+1, 2] = (int(255*float(arr[i])), int(255*float(arr[i])), int(255*float(arr[i])))
rgb_im.show()

im.save("p6.png", 'PNG')'''

#from pyyoutube import Api
#api='AIzaSyCOHR7QL19fSYppTJu8jWr9LCF2b09U7Kk'
#rint(channel_by_id.items)
#print(channel_by_id.items[0].to_dict())
#import requests
#print(api)
#r=requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id=UCcAATkbSSyV8WGYaCcIZ-HA&key=AIzaSyCOHR7QL19fSYppTJu8jWr9LCF2b09U7Kk')
#print(r.json())
#b=r.json()
#print(b['items'])
#print(r.text)
#https://discord.com/api/webhooks/747235308537512007/Mpi1KwUtMVA9Qina0SdTI7eUkl7V2uKPywiPSDeozXrgWpkGha0h50R7sGfzNUYBJqwG
'''import discord
from discord.ext import commands
from discord.ext import tasks
#import cogs
import sqlite3
from sqlite3 import Error
import time
from discord import Webhook, RequestsWebhookAdapter, File
from discord.utils import get
import config
from datetime import date
import datetime  
#import utils
import sys
import time
import io
webhook = Webhook.partial("747235308537512007","Mpi1KwUtMVA9Qina0SdTI7eUkl7V2uKPywiPSDeozXrgWpkGha0h50R7sGfzNUYBJqwG",
                                  adapter=RequestsWebhookAdapter())
webhook.send("@everyone")'''

q=chr(34)
s=[
"q=chr(34)",
"s=[",
"]",
"print(s[0])",
"print(s[1])",
"for i in range(len(s)):",
"    print(q+s[i]+q+',')",
"print(s[2])",
"for i in range(3, len(s)):",
"    print(s[i])",
]
print(s[0])
print(s[1])
for i in range(len(s)):
    print(q+s[i]+q+',')
print(s[2])
for i in range(3, len(s)):
    print(s[i])