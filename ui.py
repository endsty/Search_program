import boole_search
import vector_space
import time
from tkinter import *
from tkinter.tix import Tk, Control, ComboBox  # 升级的组合控件包
from tkinter.messagebox import showinfo, showwarning, showerror  # 各种类型的提示框
import os


class Application(Frame):
    """GUI界面"""

    def __init__(self, master=None):
        super().__init__(master)  # super代表的是父类的定义，而不是父类对象
        self.master = master
        self.text = []
        self.pack()
        self.createWidget1()
        self.createWidget2()
        self.createWidget3()


    def createWidget1(self):
        """创建组件"""
        self.frame1 = Frame(self.master)
        self.frame1.pack(fill=BOTH)
        self.mode = StringVar()
        self.mode.set('排序式检索')
        self.lable = Label(self.frame1, text='Search Mode：  ', bd=4, font=14)
        self.lable.grid(row=1, column=0)
        self.mode1 = Radiobutton(self.frame1, text='布尔查询', fg='red', variable=self.mode, value='布尔查询', font=14)
        self.mode2 = Radiobutton(self.frame1, text='排序式检索', fg='blue', variable=self.mode, value='排序式检索', font=14)
        self.mode1.grid(row=1, column=2)
        self.mode2.grid(row=1, column=3)

    def createWidget2(self):
        self.frame2 = Frame(self.master)
        self.frame2.pack(fill=BOTH)
        self.var = StringVar()
        self.lable2 = Label(self.frame2, text='搜索框：  ', font=14)
        self.lable2.grid(row=2, column=0)
        self.key_entry = Entry(self.frame2, width=80, textvariable=self.var)
        self.key_entry.grid(row=2, column=1)
        self.start_button = Button(self.frame2, text='开始搜索', font=14, width=12, bg='light blue', command=self.select)
        self.start_button.grid(row=2, column=2)

    def createWidget3(self):
        self.test = Text(self.master, height=40, relief=RIDGE, font=14)
        self.test.pack(fill=BOTH)

    def select(self):
        self.test.delete(0.0, END)
        if self.mode.get() == '排序式检索':
            self.start = time.time()
            self.text = vector_space.start_search(self.var.get())
        else:
            self.start = time.time()
            self.text = boole_search.remake_information(self.var.get())
        self.print()
        self.end = time.time()
        print('程序运行总时间为：', (self.end-self.start), 's')

    def print(self):
        os.getcwd()
        path = 'querys/'+str(self.var.get())+'.txt'
        with open(path, 'w', encoding='utf-8', errors='ignore') as f:
            for i in range(len(self.text)):
                self.test.insert(INSERT, self.text[i]+'\n')
                f.write(self.text[i]+'\n')


def main():
    root = Tk()
    root.title('智能检索')
    root.geometry('800x600')
    root.tk.eval('package require Tix')  # 引入升级包，这样才能使用升级的组合控件

    app = Application(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
