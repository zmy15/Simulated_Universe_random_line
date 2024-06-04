import tkinter as tk
from tkinter import messagebox, Scrollbar
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
from ico import encoded_image

# 指定窗口标题
WINDOW_TITLE = "崩坏：星穹铁道"
AUTHOR_WEBSITE = "https://space.bilibili.com/646510445"

input_image = 'input.png'
output_image = 'output.png'


def open_screenshot(event):
    webbrowser.open(output_image)


def open_author_website(event):
    webbrowser.open(AUTHOR_WEBSITE)


class function:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.tutorial_button = tk.Button(master, text="使用教程", command=self.show_tutorial)
        self.tutorial_button.pack(pady=10)

        self.screenshot_button = tk.Button(master, text="截图", command=self.take_screenshot)
        self.screenshot_button.pack(pady=20)

        self.author_label = tk.Label(master, text="点击关注作者：这次一定消耗6个硬币", fg="blue")
        self.author_label.pack(side="bottom", pady=10)
        self.author_label.bind("<Button-1>", open_author_website)

    def take_screenshot(self):
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

            move.move(input_image, output_image)
            # 显示截图
            img = Image.open(output_image)
            img.thumbnail((1920, 1080))  # 调整显示尺寸
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.master, image=img)
            img_label.config(image=img)
            img_label.image = img  # 防止图片被垃圾回收

            messagebox.showinfo("成功！", "路径生成成功，如果出现问题请重试！")
            success_msg = tk.Label(self.master, text="线路图已保存，点击打开", fg="blue", cursor="hand2")
            success_msg.pack()
            success_msg.bind("<Button-1>", open_screenshot)
            os.remove("input.png")

    def show_tutorial(self):
        tutorial_window = tk.Toplevel(self.master)
        tutorial_window.title("使用教程")
        tutorial_window.geometry("1280x1080")

        # 创建Canvas
        canvas = tk.Canvas(tutorial_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建滚动条
        scrollbar = tk.Scrollbar(tutorial_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 将Canvas和滚动条关联
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # 创建一个Frame来包含所有教程内容
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        tutorial_text = "使用教程:\n\n1. 如图启动模拟宇宙,注意不要挡住地图!\n2.点击截图，稍等即可生成线路\n"
        label = tk.Label(content_frame, text=tutorial_text)
        label.pack(pady=10, padx=10)

        for image_name in ["1.png", "2.png"]:
            try:
                decoded_image = base64.b64decode(encoded_images[image_name])
                image = Image.open(BytesIO(decoded_image))
                image.thumbnail((1280, 720))  # 调整显示尺寸
                tutorial_img = ImageTk.PhotoImage(image)
                img_label = tk.Label(content_frame, image=tutorial_img)
                img_label.image = tutorial_img  # 防止图片被垃圾回收
                img_label.pack(pady=10)
            except Exception as e:
                error_label = tk.Label(content_frame, text=f"无法加载教程图片: {image_name}", fg="red",
                                       font=("Arial", 12))
                error_label.pack(pady=10)

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)


def main():
    # 创建主窗口
    root = tk.Tk()
    decoded_image = base64.b64decode(encoded_image["puman.png"])
    image = Image.open(BytesIO(decoded_image))
    root.iconphoto(True, ImageTk.PhotoImage(image))
    root.title("随机线路生成工具")
    screen = function(root)
    information_label = tk.Label(root, text="模拟宇宙随机线路生成工具", fg="black")
    information_label.pack(pady=10)

    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()
