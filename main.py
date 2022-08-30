from fileinput import filename
import tkinter as tk
import os
import PIL
from PIL import Image, ImageTk

class ImageViewer():
    
    def __init__(self, window, img_files):
        self.canvas_width = 1200
        self.canvas_height = 300
        self.pcanvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.pcanvas.grid(row=0, column=0)
        
        self.acanvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.acanvas.grid(row=1, column=0)
        self.window = window


        self.button = tk.Button(window, text="문제확인", command=self.show_problem)
        self.button.grid(row=2, column=1)
        self.button = tk.Button(window, text="정답확인", command=self.check_answer)
        self.button.grid(row=2, column=2)
        self.button = tk.Button(window, text="다음문제", command=self.next_problem)
        self.button.grid(row=2, column=3)
        
        self.input_text = tk.Text(window, height=20, width=100)
        self.input_text.grid(row=2,column=0)

        self.img_files = img_files
        self.p_idx = 0
        self.sub_p_idx = 0

    def show_problem(self):
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][0])
        r_height = self.canvas_height
        r_width = self.canvas_width
        image = image.resize((r_height, r_width), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.p_on_canvas = self.pcanvas.create_image(0, 0, anchor=tk.NW, image=photo)
        # self.pcanvas.pack(side='top', expand=True,fill='both')
        
    def check_answer(self):       
        image = Image.open(self.img_files[self.p_idx][self.sub_p_idx][1])
        r_height = self.canvas_height
        r_width = self.canvas_width
        image = image.resize((r_height, r_width), PIL.Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.a_on_canvas = self.acanvas.create_image(0, 0, anchor=tk.NW, image=photo)
    
    def next_problem(self):
        sub_problem_size = len(self.img_files[self.p_idx])
        self.sub_p_idx += 1
        if self.sub_p_idx == sub_problem_size:
            self.p_idx += 1
            self.sub_p_idx = 0


window = tk.Tk()
window.title("AIExpert Exam 2022")
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
ImageViewer(window, img_files)
window.mainloop()
