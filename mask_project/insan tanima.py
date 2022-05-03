import os
import tkinter
import cv2
from tkinter import ttk
from tkinter import *
import warnings
import  numpy as np
window = tkinter.Tk()
warnings.filterwarnings("ignore")
window.state("zoom")
window.title("Dronx")
from PIL import ImageTk , Image

f2 = LabelFrame(window, bg="blue")
f2.place(x=25, y=0)
label1 = Label(f2, bg="blue")
label1.place(x=675, y=450)
label1.pack()

f4 = LabelFrame(window, bg="blue")
f4.place(x=685, y=0)
label3 = Label(f4, bg="blue")
label3.place(x=685, y=450)
label3.pack()
cap = cv2.VideoCapture("peopleCount.mp4")
sart = 1000
mog = cv2.createBackgroundSubtractorMOG2()
ksize = (5,5)
sigma =7

def yazdır():
    dosya = open("veri.txt" , mode = "w")
    dosya.write(sınır.get())
    sınır.delete(0 , "end")
sınır = Entry(window , font=("arial" , 14))
sınır.place(x = 50 , y = 560)
sınır_but = Button(window , text = "kaydet" , command = yazdır)
sınır_but.place(x = 300 ,y= 560)
bildirim = Label(window  , text = "", font=("arial" , 14) , fg = "red")
bildirim.place(x = 500 , y = 560  )
text = Label(window  , text = "İnsan sınırı" , font=("arial" , 14))
text.place(x = 50 , y = 520  )
label = Label(window, text="")
label.place(x=300, y=530)
while 1:
    people = 0
    ret ,frame = cap.read()
    frame2 = cv2.GaussianBlur( frame , ksize=ksize , sigmaX=sigma)
    mask = mog.apply(frame2)
    mask = cv2.erode(mask, kernel=None, iterations=5)

    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if(len(cnts) > 0 ):
        for cnt in cnts:
            x,y,w,h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if (area > sart):
              people = people + 1
              cv2.rectangle(frame ,(x,y) , (x+w , y+h) ,color=(0,255,0) , thickness=2)
    cv2.putText(frame , "Bulunan insanlar : "+ str(people) ,(5,20)  , cv2.FONT_HERSHEY_COMPLEX , 1 , (0,255,0) , 1 )
    img2 = cv2.resize(frame, (650, 450))
    img2 = ImageTk.PhotoImage(Image.fromarray(img2))
    label1["image"] = img2
    img3 = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    img3 = cv2.resize(img3, (650, 450))
    img3 = ImageTk.PhotoImage(Image.fromarray(img3))
    label3["image"] = img3
    dosya = open("veri.txt", mode="r")
    lines = dosya.readlines()


    label.config(text = lines[0])
    if (people >int(lines[0])):
        bildirim.config(text = "riskli ortam ")

    else :
        bildirim.config(text = "risksiz ortam")

    window.update()

