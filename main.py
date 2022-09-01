from math import ceil
import random
import tkinter as tk
from tkinter import messagebox
import os
import PIL
from PIL import Image, ImageTk

wwidth = 800
wheight = 600
class ImageViewer():
    
    def __init__(self, window, img_files):
        self.window : tk.Tk = window
        self.canvas_width = wwidth // 2
        self.canvas_height = wheight // 2
        self.img_files = img_files
        
        self.grid_pos = {
            'restart':(2,4),
            'psize':(3,4),
            'prev':(4,4),
            'next':(5,4),
            'check_answer':(6,4),
            'hide_answer':(7,4)
        }
        
        self.pcanvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
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

        self.restart_button = tk.Button(self.window, text="Restart", command=self.restart)
        self.restart_button.grid(row=self.grid_pos['restart'][0], column=self.grid_pos['restart'][1])
        self.problem_size_text = tk.Entry(self.window, width=10)
        self.problem_size_text.insert(0,f'{len(self.img_files)}')
        self.problem_size_text.grid(row=self.grid_pos['psize'][0], column=self.grid_pos['psize'][1])
        self.button1 = tk.Button(self.window, text="이전문제", command=self.prev_problem)
        self.button1.grid(row=self.grid_pos['prev'][0], column=self.grid_pos['prev'][1])
        self.button2 = tk.Button(self.window, text="다음문제", command=self.next_problem)
        self.button2.grid(row=self.grid_pos['next'][0], column=self.grid_pos['next'][1])
        self.button3 = tk.Button(self.window, text="정답확인", command=self.check_answer)
        self.button3.grid(row=self.grid_pos['check_answer'][0], column=self.grid_pos['check_answer'][1])
        self.button4 = tk.Button(self.window, text="정답숨기기", command=self.hide_answer)
        self.button4.grid(row=self.grid_pos['hide_answer'][0], column=self.grid_pos['hide_answer'][1])
        
        self.input_text = tk.Text(self.window, height=20, width=100)
        self.input_text.grid(row=3,column=2)
        
        self.var = tk.IntVar()
        self.cbutton = tk.Checkbutton(window, text='answer',variable=self.var, onvalue=1, offvalue=0, command=self.ans_count)
        self.cbutton.grid(row=self.grid_pos['next'][0], column=self.grid_pos['next'][1] - 1)
        self.ans_state = []
        
        self.l = tk.Label(window, bg='white', width=20, text='empty')
        self.l.grid(row=3,column=0)
        self.pnum = tk.Label(window, bg='white', width=20, text='empty')
        self.pnum.grid(row=4,column=0)
        self.pmode = tk.Entry(window, bg='white', width=20)
        self.pmode.insert(0,'all')
        self.pmode.grid(row=5,column=0)

        self.p_idx = 0
        self.sub_p_idx = 0
        self.psize = 0
        
        self.pimg= None
        self.aimg = None
        
        # self.shuffle(orig_img_files,41)
        # self.show_problem()
        self.pcanvas.bind_all("<MouseWheel>", self._on_mousewheel_problem)
        # self.acanvas.bind_all("<MouseWheel>", self._on_mousewheel_answer)
        
        self.restart()

    def ans_count(self):
        ans_count = 0
        if len(self.ans_state) != 0:
            self.ans_state[self.p_idx][self.sub_p_idx] = self.var.get()
            for state in self.ans_state:
                if sum(state) == len(state):
                    ans_count += 1
        self.l.config(text=f'{ans_count}/{self.psize}')
        
    def _on_mousewheel_problem(self, event):
        self.pcanvas.yview_scroll(-1*(event.delta//120), "units")
        
    def _on_mousewheel_answer(self, event):
        self.acanvas.yview_scroll(-1*(event.delta//120), "units")
        
    def shuffle(self, img_files, size, pmode):
        if pmode != 'all':
            img_files = []
            if pmode == 'ans':
                for idx, state in enumerate(self.ans_state):
                    if state[0] == 1:
                        img_files.append(self.img_files[idx])
            elif pmode == 'not':
                for idx, state in enumerate(self.ans_state):
                    if state[0] == 0:
                        img_files.append(self.img_files[idx])
            size = len(img_files)
            
        random.shuffle(img_files)
    
        return img_files[:size+1]
    def restart(self):
        psize = self.problem_size_text.get()
        self.psize = int(psize)
        pmode = self.pmode.get()
        self.img_files = self.shuffle(orig_img_files[:], self.psize, pmode)
        self.psize = len(self.img_files)
        self.p_idx = 0
        self.sub_p_idx = 0
        self.ans_state = []
        for pidx, img_file in enumerate(self.img_files):
            state = []
            for sub_pidx, sub_img_file in enumerate(img_file):
                state.append(0)
            self.ans_state.append(state)
        self.show_problem()
        self.hide_answer()
        
    def show_problem(self):
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][0])
        self.pimg = ImageTk.PhotoImage(image=image)
        x, y, new_width, new_height = self.window.grid_bbox(column=0,row=0)
        if new_width != 0 and new_height != 0:
            if new_width > self.pimg.width():
                new_width = self.pimg.width()
            self.pcanvas.config(width=new_width,height=new_height)
        else:
            self.pcanvas.config(width=self.pimg.width(),height=self.pimg.height())
        self.pcanvas.itemconfig(self.p_on_canvas, image=self.pimg)
        self.pcanvas.config(scrollregion=(0,0,self.pimg.width(),self.pimg.height()))
        if len(self.ans_state) > 0:
            if self.ans_state[self.p_idx][self.sub_p_idx] == 0:
                self.cbutton.deselect()
                self.var.set(0)
            else:
                self.cbutton.select()
                self.var.set(1)
        self.ans_count()
        self.pnum.config(text=f'Problem num : {self.p_idx+1}_{self.sub_p_idx+1}')
        
    def check_answer(self):       
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][1])
        self.aimg = ImageTk.PhotoImage(image=image)
        # self.aimg = tk.PhotoImage(file=image)
        x, y, new_width, new_height = self.window.grid_bbox(column=2,row=0)
        if new_width != 0 and new_height != 0:
            if new_width > self.aimg.width():
                new_width = self.aimg.width()
            self.acanvas.config(width=new_width,height=new_height)
        else:
            self.acanvas.config(width=self.aimg.width(),height=self.aimg.height())
        self.acanvas.config(scrollregion=(0,0,self.aimg.width(),self.aimg.height()))
        self.acanvas.itemconfig(self.a_on_canvas, image=self.aimg, state='normal')
    
    def hide_answer(self):
        self.acanvas.itemconfig('all',state='hidden')
    
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
window.geometry(f"{wwidth}x{wheight}")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(2, weight=1)

idx = 1
root_dir = f'data'
orig_img_files = []
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
                ans_file = 'a' + p_file[1:]
                # if p_num == '':
                #     ans_file = f'a{i}.png'
                # else:
                #     ans_file = f'a{i}_{p_num}.png'
                p_file = f'{root}/{p_file}'
                ans_file = f'{root}/{ans_file}'
                pa_pair_files.append((p_file, ans_file))
        orig_img_files.append(pa_pair_files) 
        
ImageViewer(window, orig_img_files)
window.mainloop()