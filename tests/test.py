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
