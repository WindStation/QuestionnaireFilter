# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import tkinter.font
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox
from GUI.build.build import basic_info
from util.HighDPI import set_dpi_awareness
from processing.Filter import Filter
from util.FileReader import read_source

set_dpi_awareness()

# OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r"GUI\build\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def start_window(username="User", test=False):
    username = "User" if username == "" else username

    window = Tk()

    window.geometry("1200x740")
    window.configure(bg="#FFFFFF")
    window.title("选择问卷文件")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=740,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1200.0,
        100.0,
        fill="#326199",
        outline="")

    canvas.create_text(
        121.0,
        25.0,
        anchor="nw",
        text="Metric",
        fill="#FFFFFF",
        font=("Consolas", 40 * -1)
    )

    canvas.create_text(
        802.0,
        29.0,
        anchor="nw",
        text="Welcome, " + username,
        fill="#FFFFFF",
        font=("Microsoft YaHei", 32 * -1)
    )

    canvas.create_text(
        614.0,
        312.0,
        anchor="nw",
        text="选择问卷文件",
        fill="#000000",
        font=("Microsoft YaHei", 48 * -1, "bold")
    )

    def select_btn_clicked():
        filename = filedialog.askopenfilename(title="Select XLSX file",
                                              filetypes=(("XLSX files", "*.xlsx"), ("ALL", "*.*"),))
        print(filename)
        if filename is None or filename == "":
            return
        elif filename[-5:] != ".xlsx":
            messagebox.showinfo("Error", "请选择正确格式的文件。")
            return
        filter = Filter(read_source(filename), filename.split("/")[-1][:-5], test=True)
        if test:
            filter.build_basic_info()
            filter.build_condition()
        window.destroy()
        basic_info.start_window(filename, filter)

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=select_btn_clicked,
        relief="flat"
    )
    button_1.place(
        x=637.0,
        y=449.0,
        width=242.0,
        height=108.0
    )

    canvas.create_rectangle(
        24.0,
        128.0,
        373.0,
        713.0,
        fill="#326299",
        outline="")

    canvas.create_text(
        38.0,
        162.0,
        anchor="nw",
        width=321,
        text="问卷筛选 · 说明：\n\n当前支持使用xlsx格式的文件进行问卷筛选。需要问卷的问题按列分布，而回答按行分布。\n当前已支持的筛选条件包括：\n1. 作答时间长短\n2. 强制题选项\n3. 重复题选项\n4. 选项重复率\n在选择文件后，请按照提示，填写问卷的基本信息，和筛选的具体参数。",
        fill="#FFFFFF",
        font=("Microsoft YaHei", 20 * -1)
    )

    canvas.create_text(
        47.0,
        566.0,
        anchor="nw",
        text="Designed & Developed By",
        fill="#FFFFFF",
        font=("Consolas Bold", 24 * -1)
    )

    canvas.create_text(
        126.0,
        611.0,
        anchor="nw",
        text="WindStation",
        fill="#FFFFFF",
        font=("Consolas Bold", 24 * -1)
    )

    canvas.create_text(
        521.0,
        173.0,
        anchor="nw",
        text="Step. 1",
        fill="#000000",
        font=("Consolas", 48 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    start_window()
