from math import ceil
from random import random
import tkinter as tk
from tkinter import messagebox
import os
import PIL
from PIL import Image, ImageTk

class ImageViewer():
    
    def __init__(self, window, img_files):
        self.window : tk.Tk = window
        self.canvas_width = 900
        self.canvas_height = 500
        
        self.pcanvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height+100)
        self.p_on_canvas = self.pcanvas.create_image(0, 0, anchor=tk.NW)
        self.pcanvas.grid(row=0, column=0)
        
        self.x_scrollbar1 = tk.Scrollbar(self.window,orient='horizontal')
        self.x_scrollbar1.grid(row=1, column=0,sticky=tk.S+tk.EW)
        self.y_scrollbar1 = tk.Scrollbar(self.window,orient='vertical')
        self.y_scrollbar1.grid(row=0, column=1,sticky=tk.E+tk.NS)
        
        self.y_scrollbar1.config(command=self.pcanvas.yview)
        self.x_scrollbar1.config(command=self.pcanvas.xview)
        self.pcanvas.config(
            yscrollcommand=self.y_scrollbar1.set, 
            xscrollcommand=self.x_scrollbar1.set)
        
        self.acanvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height-100)
        self.a_on_canvas = self.acanvas.create_image([0, 0], anchor=tk.NW)
        self.acanvas.grid(row=0, column=2)
        
        self.x_scrollbar2 = tk.Scrollbar(self.window,orient='horizontal')
        self.x_scrollbar2.grid(row=1, column=2,sticky=tk.S+tk.EW)
        self.y_scrollbar2 = tk.Scrollbar(self.window,orient='vertical')
        self.y_scrollbar2.grid(row=0, column=3,sticky=tk.E+tk.NS)
        
        self.x_scrollbar2.config(command=self.acanvas.xview)
        self.y_scrollbar2.config(command=self.acanvas.yview)
        self.acanvas.config(
            yscrollcommand=self.y_scrollbar2.set,
            xscrollcommand=self.x_scrollbar2.set)

        self.button = tk.Button(self.window, text="이전문제", command=self.prev_problem)
        self.button.grid(row=2, column=0)
        self.button = tk.Button(self.window, text="다음문제", command=self.next_problem)
        self.button.grid(row=2, column=1)
        self.button = tk.Button(self.window, text="정답확인", command=self.check_answer)
        self.button.grid(row=3, column=0)
        
        self.input_text = tk.Text(self.window, height=20, width=100)
        self.input_text.grid(row=3,column=2)

        self.img_files = img_files
        self.p_idx = 0
        self.sub_p_idx = 0
        
        self.pimg= None
        self.aimg = None
        
        self.show_problem()

    def show_problem(self):
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][0])
        # image = self.img_files[self.p_idx][self.sub_p_idx][0]
        # img_width = image.width
        # img_height = image.height
        # r_height = self.canvas_height
        # r_width = self.canvas_width
        # print('img',img_width,img_height)
        # print('before', r_width, r_height)
        # # if img_width > r_width:
        # #     delta = img_width - r_width
        # #     r_height -= int(delta * (img_height / img_width))
        # #     print('after',r_width, r_height)
        # image = image.resize((r_height, r_width), Image.ANTIALIAS)
        self.pimg = ImageTk.PhotoImage(image=image)
        # self.pimg = tk.PhotoImage(file=image)
        # x_rate = ceil(self.pimg.width() /self.canvas_width)
        # y_rate = ceil(self.pimg.height() /self.canvas_height)
        # print(x_rate,y_rate)
        # rate = max(x_rate,y_rate)
        # self.pimg = self.pimg.subsample(2)
        # self.p_on_canvas = self.pcanvas.create_image(0, 0, anchor=tk.NW, image=photo)
        # self.pcanvas.config(width=self.pimg.width())
        # self.acanvas.config(width=self.window.winfo_width() - self.pimg.width())
        self.pcanvas.itemconfig(self.p_on_canvas, image=self.pimg)
        self.pcanvas.config(scrollregion=(0,0,self.pimg.width(),self.pimg.height()))
        
    def check_answer(self):       
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][1])
        self.aimg = ImageTk.PhotoImage(image=image)
        # self.aimg = tk.PhotoImage(file=image)
        self.acanvas.config(scrollregion=(0,0,self.aimg.width(),self.aimg.height()))
        self.acanvas.itemconfig(self.a_on_canvas, image=self.aimg, state='normal')
    
    def next_problem(self):
        sub_problem_size = len(self.img_files[self.p_idx])
        self.sub_p_idx += 1
        if self.sub_p_idx == sub_problem_size:
            self.p_idx += 1
            self.sub_p_idx = 0
        if self.p_idx == len(self.img_files):
            self.p_idx = len(self.img_files) - 1
            messagebox.showinfo('info','마지막 문제 입니다.')
        self.show_problem()
        self.acanvas.itemconfig('all',state='hidden')
    
    def prev_problem(self):
        self.sub_p_idx -= 1
        if self.sub_p_idx < 0:
            self.p_idx -= 1
            self.sub_p_idx = 0
        if self.p_idx < 0:
            self.p_idx = 0
            messagebox.showinfo('info','처음 문제 입니다.')
        self.show_problem()
        self.acanvas.itemconfig('all',state='hidden')

window = tk.Tk()
window.title("AIExpert Exam 2022")
window.geometry("1920x1080")

idx = 1
root_dir = f'data'
img_files = []
for i in range(41):
    for (root, dirs, files) in os.walk(root_dir+f'/{i}'):
        pa_pair_files = []
        for file_name in files:
            if file_name.startswith('p'):
                p_num = file_name.split('.')[0].split('_')
                if len(p_num) > 1:
                    p_num = p_num[1]
                else:
                    p_num =''
                p_file = file_name
                if p_num == '':
                    ans_file = f'a{i}.png'
                else:
                    ans_file = f'a{i}_{p_num}.png'
                p_file = f'{root}/{p_file}'
                ans_file = f'{root}/{ans_file}'
                pa_pair_files.append((p_file, ans_file))
        img_files.append(pa_pair_files) 

def shuffle(img_files, size):
    res = []
    # min_idx = 0
    max_idx = len(img_files) - 1
    visited = [False for _ in range(max_idx+1)]
    for _ in range(size):
        rand_idx = int(random() * max_idx)
        while visited[rand_idx]:
            rand_idx = int(random() * max_idx)
        visited[rand_idx] = True
        res.append(img_files[rand_idx])
    
    return res
img_files = shuffle(img_files, 20)
ImageViewer(window, img_files)
window.mainloop()