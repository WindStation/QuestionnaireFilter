import tkinter as tk
from ctypes import windll
from tkinter import filedialog


def on_button_click():
    input_text = entry.get()
    label_result.config(text="Hello, " + input_text + "!")
    # message_box = tk.Message(root, width=100)
    # message_box.config(text="This is a test, with text=" + input_text)
    # message_box.config()
    # message_box.pack()


def select_file():
    selected_path = filedialog.askopenfilename()
    print(selected_path)


def set_dpi_awareness():
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        try:
            windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass


set_dpi_awareness()

# 创建主窗口
root = tk.Tk()
root.title("简单GUI示例")

# 设置缩放
# root.tk_setScale(1.25)
root.geometry("800x800")

# 创建标签
label = tk.Label(root, text="请输入您的名字:")
label.pack(pady=30, padx=10)

# 创建输入框
entry = tk.Entry(root)
entry.pack(pady=10)

# 创建按钮
button = tk.Button(root, text="点击我", command=on_button_click, width=10, height=2)
button.pack(side=tk.LEFT, padx=60, pady=10)

# 创建结果标签
label_result = tk.Label(root, text="")
label_result.pack(pady=10)

# 创建列表框
# listbox = tk.Listbox(root)
# for item in ["苹果", "香蕉", "橙子", "葡萄"]:
#     listbox.insert(tk.END, item)
# listbox.pack(side=tk.RIGHT, pady=10, padx=60)

openfile_btn = tk.Button(root, text="选择文件", command=select_file, width=10, height=2)
openfile_btn.pack(pady=10)

listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
for item in ["1", "2", "3", "4", "5"]:
    listbox.insert(tk.END, item)
listbox.pack()


def select_all():
    listbox.select_set(0, tk.END)


def reverse_all():
    pass


def print_info():
    pass


all_btn = tk.Button(root, text="全选", command=select_all)
all_btn.pack()

tk.Button(root, text="查看情况", command=print_info)

# 运行主循环
if __name__ == '__main__':
    root.mainloop()
