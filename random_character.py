import atexit
import json
import os
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
from io import BytesIO
import embedded_data


# 解码角色信息 JSON
def decode_characters():
    return json.loads(base64.b64decode(embedded_data.characters_json_base64).decode('utf-8'))


characters = decode_characters()


# 解码图片
def decode_image(base64_str):
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data))


# 解码并写入配置文件
def decode_config():
    config = json.loads(base64.b64decode(embedded_data.config_json_base64).decode('utf-8'))
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    return config


# 读取配置文件
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        user_config = json.load(f)
except FileNotFoundError:
    user_config = decode_config()


def save_config_to_file():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(user_config, f, ensure_ascii=False, indent=4)


def delete_config_file():
    if os.path.exists('config.json'):
        os.remove('config.json')


# 注册程序结束时删除 config.json 文件
atexit.register(delete_config_file)


class random_character:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1280x800")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.result_label = tk.Label(self.frame, text="", wraplength=300)
        self.result_label.pack()

        self.image_label = tk.Label(self.frame)
        self.image_label.pack()

        self.tutorial_button = tk.Button(master, text="随机配置选项", command=self.open_config_window)
        self.tutorial_button.pack(side="bottom", pady=10)

        self.tutorial_button = tk.Button(master, text="随机", command=self.draw_character)
        self.tutorial_button.pack(pady=10)

        self.current_candidates = []

    def update_candidates(self):
        attributes = user_config['attributes']
        fates = user_config['fates']
        included_names = user_config['included_names']

        self.current_candidates = [char for char in characters
                                   if char['attribute'] in attributes
                                   and char['fate'] in fates
                                   and char['name'] in included_names]

    # 抽取角色的函数
    def draw_character(self):
        if not self.current_candidates:
            self.update_candidates()

        if not self.current_candidates:
            self.result_label.config(text="没有符合条件的角色")
            self.image_label.config(image='')
            return

        selected_character = random.choice(self.current_candidates)
        self.current_candidates.remove(selected_character)

        self.result_label.config(
            text=f"{selected_character['name']}\n属性: {selected_character['attribute']}\n命途: {selected_character['fate']}")

        img = decode_image(embedded_data.images_base64[selected_character['name']])
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def open_config_window(self):
        def save_config():
            user_config['attributes'] = [attr for attr, var in attribute_checkbuttons.items() if var.get() == 1]
            user_config['fates'] = [fate for fate, var in fate_checkbuttons.items() if var.get() == 1]
            user_config['included_names'] = [name for name, var in name_checkbuttons.items() if var.get() == 1]
            self.current_candidates = []
            save_config_to_file()
            config_window.destroy()

        config_window = tk.Toplevel(self.master)
        config_window.title("配置抽取条件")
        config_window.geometry("600x800")

        # 创建滚动条和画布
        canvas = tk.Canvas(config_window)
        scrollbar = ttk.Scrollbar(config_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        attribute_frame = tk.LabelFrame(scrollable_frame, text="选择属性:")
        attribute_frame.pack(fill="both", expand=True)

        attribute_checkbuttons = {}
        attributes = set(char['attribute'] for char in characters)
        for i, attr in enumerate(attributes):
            var = tk.IntVar(value=1 if not user_config['attributes'] or attr in user_config['attributes'] else 0)
            cb = tk.Checkbutton(attribute_frame, text=attr, variable=var)
            cb.grid(row=i // 4, column=i % 4, sticky='w')
            attribute_checkbuttons[attr] = var

        fate_frame = tk.LabelFrame(scrollable_frame, text="选择命途:")
        fate_frame.pack(fill="both", expand=True)

        fate_checkbuttons = {}
        fates = set(char['fate'] for char in characters)
        for i, fate in enumerate(fates):
            var = tk.IntVar(value=1 if not user_config['fates'] or fate in user_config['fates'] else 0)
            cb = tk.Checkbutton(fate_frame, text=fate, variable=var)
            cb.grid(row=i // 4, column=i % 4, sticky='w')
            fate_checkbuttons[fate] = var

        name_frame = tk.LabelFrame(scrollable_frame, text="选择角色:")
        name_frame.pack(fill="both", expand=True)

        name_checkbuttons = {}
        for i, character in enumerate(characters):
            var = tk.IntVar(
                value=1 if not user_config['included_names'] or character['name'] in user_config[
                    'included_names'] else 0)
            cb = tk.Checkbutton(name_frame, text=character['name'], variable=var)
            cb.grid(row=i // 4, column=i % 4, sticky='w')
            name_checkbuttons[character['name']] = var

        save_button = tk.Button(scrollable_frame, text="保存配置", command=save_config)
        save_button.pack()

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
