import pygame, time, random, sys
from tkinter import *
from tkinter import messagebox
import tank as tank
import sleepycat_718 as cat
import threading  # 导入多线程模块


class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title('Game')
        self.root.iconbitmap('kyoto u.ico')
        self.root.update()
        self.root.config(background="grey")  ##feeeed
        width = 500
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size_geo)
        self.interface()

    def interface(self):
        """"界面编写位置"""
        self.label = Label(self.root, width=20, height=1, text='Game', fg='white', bg='#34A2FE',
                           font=('TimesNewRoman', 30),
                           justify='center')
        self.label.pack(anchor=CENTER)
        self.button1 = Button(self.root, width=20, height=1, text='Tank', activeforeground="red",
                              activebackground="pink", command=self.start, pady=1,
                              justify='center')
        self.button1.pack(anchor=CENTER,pady=20)
        self.button2 = Button(self.root, width=20, height=1, text='Cat', activeforeground="red",
                              activebackground="pink", command=self.cat,
                              justify='center')
        self.button2.pack(anchor=CENTER)

    def start(self):
        self.T = threading.Thread(target=self.entrance())  # 多线程
        self.T.setDaemon(True)  # 线程守护，即主进程结束后，此线程也结束。否则主进程结束子进程不结束
        self.T.start()  # 启动

    def entrance(self):
        self.root.geometry("500x500-10000-10000")#将窗口移到界面外
        #self.root.destroy()
        self.root.update()
        tank.MainGame().startGame()

    def entrance2(self):
        self.root.geometry("500x500-10000-10000")#将窗口移到界面外
        #self.root.destroy()
        self.root.update()
        cat.start_game()

    def cat(self):
        self.T = threading.Thread(target=self.entrance2())  # 多线程
        self.T.setDaemon(True)  # 线程守护，即主进程结束后，此线程也结束。否则主进程结束子进程不结束
        self.T.start()  # 启动


if __name__ == '__main__':
    root = GUI()
    root.root.mainloop()