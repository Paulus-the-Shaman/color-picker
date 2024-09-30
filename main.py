import customtkinter as ctk
import tkinter as tk
import lib.colour_lib as colour_lib
import math
from PIL import ImageTk, Image
import pyperclip
import os
import numpy


class Color_Scroll_2(ctk.CTkFrame):
    def __init__(self, master=None, color_book: str = None):
        super().__init__(master=master, width=25 * 15, height=400, fg_color='#41474B', bg_color='#41474B',
                         corner_radius=0)
        self.master_ = master
        self.canvas = tk.Canvas(master=self, width=(25 * 15) + 4, height=400, bg='#41474B', borderwidth=0)
        self.scroll_bar = ctk.CTkScrollbar(master=self, orientation='vertical',
                                           fg_color='#41474B', button_color='#7B8085',
                                           button_hover_color='#8C9093',
                                           command=self.canvas.yview)

        self.scroll_bar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Button-1>', lambda e: self.clicked(e))
        color_book = "color_books/" + color_book
        self.data = self.file_open(color_book)  # default color book

        self.canvas.pack()
        self.place(x=0, y=0)

        self.scroll_y = 0
        self.x = 0
        self.y = 0
        self.offset = 2
        import lib.image_gen as ImgGen
        self.y = ImgGen.img_gen(self.data)[1]
        self.image = ImageTk.PhotoImage(Image.open('src/paint_box.png'), size=((15 * 25) + 1, (15 * self.y) + 16))
        self.canvas.create_image(self.offset, self.offset, image=self.image, anchor='nw')
        self.scroll_bar.bind("<Configure>",
                             lambda e: self.canvas.configure(
                                 scrollregion=(0, 0, 25 * 15, self.y * 15 + self.offset * 10)))

    def box(self, x, y, color):
        self.canvas.create_rectangle((x * 15) + self.offset, (y * 15) + self.offset, (x * 15) + 15 + self.offset,
                                     (y * 15) + 15 + self.offset, fill=color)

    def clicked(self, e):
        canvas = e.widget
        e.x = canvas.canvasx(e.x)
        e.y = canvas.canvasy(e.y)
        x = math.floor((e.x - self.offset) / 15)
        y = math.floor((e.y - self.offset) / 15)

        result = x + (y * 25)
        self.master_.master.master_.color_changer_pantone_box(self.data[result])

    def file_open(self, file_path: str):
        with open(file_path, 'r') as f:
            data = f.readlines()
        for i in range(len(data)):
            data[i] = data[i][0:7]

        data = numpy.array(data)
        return data


class Color_book_tab(ctk.CTkTabview):
    def __init__(self, master=None):
        super().__init__(master=master, width=420, height=440, fg_color='transparent', corner_radius=0,
                         segmented_button_fg_color='#363432',
                         segmented_button_selected_color='#1b1918', text_color='#cccccc',
                         segmented_button_unselected_color='#363432', anchor='w')
        self.master_ = master
        for file in os.listdir('color_books'):
            if file[-4:] == '.txt':
                self.add(file[0:-4])
                Color_Scroll_2(master=self.tab(file[0:-4]), color_book=file)

        self.place(x=0, y=-10)


class Slider_frame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, corner_radius=0, fg_color='transparent')
        self.master_ = master
        self.grid_columnconfigure(index=0, weight=1, uniform='c')
        self.grid_columnconfigure(index=1, weight=1, uniform='c')
        self.grid_columnconfigure(index=2, weight=1, uniform='c')
        self.grid_columnconfigure(index=3, weight=1, uniform='c')
        self.grid_columnconfigure(index=4, weight=1, uniform='c')
        self.grid_columnconfigure(index=5, weight=1, uniform='c')
        self.grid_columnconfigure(index=6, weight=1, uniform='c')
        self.grid_rowconfigure(index=0, weight=1, uniform='c')

        self.red = None
        self.green = None
        self.blue = None

        self.slider_height = 330
        self.slider_color_no_progress = '#242424'
        self.red_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                        progress_color='#f7584d',
                                        from_=0,
                                        to=255,
                                        fg_color=self.slider_color_no_progress, button_color='#f7584d',
                                        button_hover_color='#d94d43',
                                        command=lambda e: self.set_color_rgb(), border_color='#242424', border_width=0)
        self.green_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                          progress_color='#72f74d',
                                          from_=0,
                                          to=255,
                                          fg_color=self.slider_color_no_progress, button_color='#72f74d',
                                          button_hover_color='#5ec940',
                                          command=lambda e: self.set_color_rgb(), border_color='#242424',
                                          border_width=0)
        self.blue_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                         progress_color='#4d86f7',
                                         from_=0,
                                         to=255,
                                         fg_color=self.slider_color_no_progress, button_color='#4d86f7',
                                         button_hover_color='#4070cf',
                                         command=lambda e: self.set_color_rgb(), border_color='#242424', border_width=0)

        self.h_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                      progress_color='#F1B2DC',
                                      from_=0,
                                      to=1,
                                      fg_color=self.slider_color_no_progress, button_color='#F1B2DC',
                                      button_hover_color='#bf8eaf',
                                      command=lambda e: self.set_color_hvx(), border_color='#242424', border_width=0)
        self.v_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                      progress_color='#BF9BDE',
                                      from_=0,
                                      to=1,
                                      fg_color=self.slider_color_no_progress, button_color='#BF9BDE',
                                      button_hover_color='#8f74a6',
                                      command=lambda e: self.set_color_hvx(), border_color='#242424', border_width=0)
        self.s_slider = ctk.CTkSlider(master=self, orientation='vertical', height=self.slider_height,
                                      progress_color='#74D1EA',
                                      from_=0,
                                      to=1,
                                      fg_color=self.slider_color_no_progress, button_color='#74D1EA',
                                      button_hover_color='#5194a6',
                                      command=lambda e: self.set_color_hvx(), border_color='#242424', border_width=0)

        self.red_slider.grid(row=0, column=0)
        self.green_slider.grid(row=0, column=1)
        self.blue_slider.grid(row=0, column=2)

        self.h_slider.grid(row=0, column=4)
        self.s_slider.grid(row=0, column=5)
        self.v_slider.grid(row=0, column=6)

    def set_color_rgb(self):
        data = colour_lib.rgb_to_hsv(self.red_slider.get(), self.green_slider.get(), self.blue_slider.get())
        self.h_slider.set(data[0])
        self.s_slider.set(data[1])
        self.v_slider.set(data[2])
        self.master_.master_.color_changer_rbg_sliders(self.red_slider.get(),
                                                       self.green_slider.get(),
                                                       self.blue_slider.get())

    def set_color_hvx(self):
        data = colour_lib.hsv_to_rgb(self.h_slider.get(), self.s_slider.get(), self.v_slider.get())
        for x in range(0, len(data)):
            data[x] = data[x] * 255

        self.red_slider.set(data[0])
        self.green_slider.set(data[1])
        self.blue_slider.set(data[2])
        self.master_.master_.color_changer_rbg_sliders(*data)


class Value_disp_frame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, corner_radius=0, fg_color='transparent')
        self.master_ = master

        self.grid_columnconfigure(index=0, weight=2, uniform='b')
        self.grid_columnconfigure(index=1, weight=2, uniform='b')
        self.grid_columnconfigure(index=2, weight=1, uniform='b')

        self.selected_color_disp = ctk.CTkFrame(master=self, width=50, height=50, corner_radius=0)
        self.selected_color_disp.grid(row=0, column=0, padx=5, pady=1 + 3)

        self.selected_color_hex = ctk.CTkLabel(master=self, width=0, height=20, fg_color='transparent',
                                               text_color='#111111', corner_radius=0)
        self.selected_color_hex.grid(row=0, column=1, pady=0 + 3)
        self.selected_color_hex.configure(text='-------')

        self.copy_button = ctk.CTkButton(master=self, width=30, height=30,
                                         image=ctk.CTkImage(light_image=Image.open('src/copy.png'), dark_image=Image.open('src/copy.png'), size=(30, 30)), text='',
                                         command=lambda: pyperclip.copy(self.selected_color_hex.cget('text')),
                                         fg_color='transparent', hover_color='#cfcfcf')
        self.copy_button.grid(row=0, column=2)


class Color_sliders(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master=master, width=210, fg_color='transparent')
        self.master_ = master
        self.grid_rowconfigure(index=0, weight=1, uniform='a')
        self.grid_rowconfigure(index=1, weight=1, uniform='a')
        self.grid_rowconfigure(index=2, weight=1, uniform='a')
        self.grid_rowconfigure(index=3, weight=1, uniform='a')
        self.grid_rowconfigure(index=4, weight=1, uniform='a')
        self.grid_rowconfigure(index=5, weight=1, uniform='a')
        self.grid_rowconfigure(index=6, weight=1, uniform='a')
        self.grid_columnconfigure(index=0, weight=1, uniform='a')

        self.slider_frame = Slider_frame(master=self)
        self.value_display_frame = Value_disp_frame(master=self)

        self.pack(side='right', padx=5)
        self.slider_frame.grid(row=0, column=0, rowspan=6, sticky='nwes')
        self.value_display_frame.grid(row=6, column=0, sticky='nwes')
        self.slider_frame.grid_propagate(False)
        self.value_display_frame.grid_propagate(False)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('615x432')
        self.configure(fg_color='#41474B')

        self.color_scroll = Color_book_tab(master=self)
        self.color_sliders_panel = Color_sliders(master=self)

    def color_changer_rbg_sliders(self, r, g, b):
        hex_color = colour_lib.rgb_to_hex(r, g, b)
        self.color_sliders_panel.value_display_frame.selected_color_disp.configure(fg_color=hex_color)
        self.color_sliders_panel.value_display_frame.selected_color_hex.configure(text=hex_color.upper())

    def color_changer_pantone_box(self, color):
        self.color_sliders_panel.value_display_frame.selected_color_disp.configure(fg_color=color)
        color_rgb = colour_lib.hex_to_rgb(color)
        self.color_sliders_panel.slider_frame.red_slider.set(color_rgb[0])
        self.color_sliders_panel.slider_frame.green_slider.set(color_rgb[1])
        self.color_sliders_panel.slider_frame.blue_slider.set(color_rgb[2])

        color_hvs = colour_lib.rgb_to_hsv(*color_rgb)
        self.color_sliders_panel.slider_frame.h_slider.set(color_hvs[0])
        self.color_sliders_panel.slider_frame.s_slider.set(color_hvs[1])
        self.color_sliders_panel.slider_frame.v_slider.set(color_hvs[2])

        self.color_sliders_panel.value_display_frame.selected_color_hex.configure(text=color.upper())

    def color_changer_text_box(self, color):
        print(color)
        print(len(color))

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
