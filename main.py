import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygetwindow as gw
import pyautogui
import webbrowser
import base64
import move
from io import BytesIO
import os

# 从 encoded_images.py 导入图片数据
from encoded_images import encoded_images


# 指定窗口标题
WINDOW_TITLE = "崩坏：星穹铁道"
AUTHOR_WEBSITE = "https://space.bilibili.com/646510445"

input_image = 'input.png'
output_image = 'output.png'


def open_screenshot(event):
    webbrowser.open(output_image)


def open_author_website(event):
    webbrowser.open(AUTHOR_WEBSITE)


def take_screenshot():
    window = gw.getWindowsWithTitle(WINDOW_TITLE)

    if not window:
        messagebox.showerror("错误", f"未找到标题为 '{WINDOW_TITLE}' 的窗口。")
    else:
        window = window[0]

        # 获取窗口的位置和尺寸
        left, top, right, bottom = window.left, window.top, window.right, window.bottom

        # 计算窗口的宽度和高度
        width = right - left
        height = bottom - top

        # 截取窗口区域的截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 保存截图
        screenshot_path = "input.png"
        screenshot.save(screenshot_path)

        move.main(input_image, output_image)
        # 显示截图
        img = Image.open(output_image)
        img.thumbnail((1920, 1080))  # 调整显示尺寸
        img = ImageTk.PhotoImage(img)

        img_label.config(image=img)
        img_label.image = img  # 防止图片被垃圾回收

        messagebox.showinfo("成功！", "路径生成成功，如果出现问题请重试！")
        success_msg = tk.Label(root, text="截图已保存，点击打开", fg="blue", cursor="hand2")
        success_msg.pack()
        success_msg.bind("<Button-1>", open_screenshot)
        os.remove("input.png")


def show_tutorial():
    tutorial_window = tk.Toplevel(root)
    tutorial_window.title("使用教程")
    tutorial_text = "使用教程:\n\n1. 如图启动模拟宇宙,注意不要挡住地图!\n2.点击截图，稍等即可生成线路\n"
    label = tk.Label(tutorial_window, text=tutorial_text, justify="left")
    label.pack(pady=10, padx=10)
    for image_name in ["1.png", "2.png"]:
        try:
            decoded_image = base64.b64decode(encoded_images[image_name])
            image = Image.open(BytesIO(decoded_image))
            image.thumbnail((1280, 720))  # 调整显示尺寸
            tutorial_img = ImageTk.PhotoImage(image)
            img_label = tk.Label(tutorial_window, image=tutorial_img)
            img_label.image = tutorial_img  # 防止图片被垃圾回收
            img_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(tutorial_window, text=f"无法加载教程图片: {image_name}", fg="red",
                                   font=("Arial", 12))
            error_label.pack(pady=10)


# 创建主窗口
root = tk.Tk()
root.title("随机线路生成工具")

information_label = tk.Label(root, text="模拟宇宙随机线路生成工具", fg="black")
information_label.pack(pady=10)

tutorial_button = tk.Button(root, text="使用教程", command=show_tutorial)
tutorial_button.pack(pady=10)

# 创建和放置控件
screenshot_button = tk.Button(root, text="截图", command=take_screenshot)
screenshot_button.pack(pady=20)

img_label = tk.Label(root)
img_label.pack(pady=10)

# 添加作者信息
author_label = tk.Label(root, text="点击关注作者：这次一定消耗6个硬币", fg="blue")
author_label.pack(side="bottom", pady=10)
author_label.bind("<Button-1>", open_author_website)

# 运行主循环
root.mainloop()