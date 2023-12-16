# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, ttk, messagebox
from util.HighDPI import set_dpi_awareness
from processing.Filter import Filter
from util.FileReader import read_source
from util.JsonIO import write_json
from GUI.build.build.query import query_basic
from GUI.build.build import param_info

set_dpi_awareness()

# OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r"GUI\build\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def start_window(filename, filter: Filter = None):
    window = Tk()

    window.geometry("1200x740")
    window.configure(bg="#FFFFFF")
    window.title("填写问卷基本信息")

    only_filename = filename.split("/")[-1]

    # INIT
    # 分两种情况：
    # 第一种是按顺序从前向后进入这个界面，此时所有项都待填
    # 第二种是从失败界面跳转回来，这时应该已经有记录

    filter = Filter(read_source(filename), only_filename) if filter is None else filter
    questions_list = filter.get_questionnaire_info()

    basic_info_dict = {
        "IndexColName": filter.idx_col_name,
        "TimeColName": filter.time_col_name,
        "TargetColIdx": filter.target_idx
    }

    # INIT OVER

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
        776.5,
        33.0,
        anchor="n",
        text=only_filename,
        fill="#FFFFFF",
        font=("Microsoft YaHei", 24 * -1),
    )

    canvas.create_text(
        121.0,
        25.0,
        anchor="nw",
        text="Metric",
        fill="#FFFFFF",
        font=("Consolas", 40 * -1)
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
        width=321,
        anchor="nw",
        text="问卷筛选 · 说明：\n\n在此界面，你需要完成以下基本信息的填写：\n 1. 代表问卷中“序号”的列\n 2. 代表问卷中“作答时间”的列。\n 3. 选择所有要参与查重筛选的问题列。\n\n每完成一项选择，其后面的指示灯会变为绿色。全部选择完毕后，可以继续进行下一步。",
        fill="#FFFFFF",
        font=("Microsoft YaHei", 20 * -1)
    )

    canvas.create_text(
        126.0,
        650.0,
        anchor="nw",
        text="WindStation",
        fill="#FFFFFF",
        font=("Consolas Bold", 24 * -1)
    )

    canvas.create_text(
        47.0,
        605.0,
        anchor="nw",
        text="Designed & Developed By",
        fill="#FFFFFF",
        font=("Consolas Bold", 24 * -1)
    )

    canvas.create_text(
        442.0,
        138.0,
        anchor="nw",
        text="Step. 2",
        fill="#000000",
        font=("Consolas", 48 * -1)
    )

    canvas.create_text(
        722.0,
        134.0,
        anchor="nw",
        text="填写基本信息",
        fill="#000000",
        font=("Microsoft YaHei", 40 * -1)
    )

    dot_1 = canvas.create_text(
        861.0,
        240.0,
        # 所有点号都要-65的高度
        anchor="nw",
        text="·",
        fill="#FF0000" if basic_info_dict["IndexColName"] is None else "#00FF00",
        font=("Microsoft YaHei", 128 * -1)
    )

    dot_2 = canvas.create_text(
        861.0,
        327.0,
        anchor="nw",
        text="·",
        fill="#FF0000" if basic_info_dict["TimeColName"] is None else "#00FF00",
        font=("Microsoft YaHei", 128 * -1)
    )

    dot_3 = canvas.create_text(
        861.0,
        413.0,
        anchor="nw",
        text="·",
        fill="#FF0000" if basic_info_dict["TargetColIdx"] is None else "#00FF00",
        font=("Microsoft YaHei", 128 * -1)
    )

    canvas.create_text(
        512.0,
        309.0,
        anchor="nw",
        text="问卷中代表“序号”的列",
        fill="#000000",
        font=("Microsoft YaHei", 28 * -1)
    )

    canvas.create_text(
        459.0,
        398.0,
        anchor="nw",
        text="问卷中代表“作答时长”的列",
        fill="#000000",
        font=("Microsoft YaHei", 28 * -1)
    )

    canvas.create_text(
        512.0,
        483.0,
        anchor="nw",
        text="所有要参与筛选的问题列",
        fill="#000000",
        font=("Microsoft YaHei", 28 * -1)
    )

    def ask_for_id():
        biq = query_basic.BasicIdQuery(questions_list, "选择序号列")
        window.wait_window(biq)
        result = biq.result  # 问题列的名称
        basic_info_dict["IndexColName"] = result
        if result is None or result == "":
            canvas.itemconfig(dot_1, fill="#FF0000")
            return
        canvas.itemconfig(dot_1, fill="#00FF00")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    select_id_btn = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=ask_for_id,
        relief="flat"
    )
    select_id_btn.place(
        x=983.0,
        y=309.0,
        width=138.0,
        height=52.0
    )

    def ask_for_time():
        biq = query_basic.BasicIdQuery(questions_list, "选择作答时间列")
        window.wait_window(biq)
        result = biq.result  # 时间列的名称
        basic_info_dict["TimeColName"] = result
        if result is None or result == "":
            canvas.itemconfig(dot_2, fill="#FF0000")
            return
        canvas.itemconfig(dot_2, fill="#00FF00")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    select_time_btn = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=ask_for_time,
        relief="flat"
    )
    select_time_btn.place(
        x=983.0,
        y=395.0,
        width=138.0,
        height=52.0
    )

    def ask_for_question():
        tq = query_basic.TargetQuery(questions_list)
        window.wait_window(tq)
        result_list = tq.result_list
        basic_info_dict["TargetColIdx"] = result_list
        if result_list is None:
            canvas.itemconfig(dot_3, fill="#FF0000")
            return
        canvas.itemconfig(dot_3, fill="#00FF00")

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    select_ques_btn = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=ask_for_question,
        relief="flat"
    )
    select_ques_btn.place(
        x=983.0,
        y=481.0,
        width=138.0,
        height=52.0
    )

    def confirm():
        complete = True
        for key in basic_info_dict.keys():
            if basic_info_dict[key] is None:
                complete = False
                break
        if not complete:
            messagebox.showinfo("Error", message="还有未完成的项目，请确保所有项都正确填写。")
            return
        write_json("json/Basic.json", basic_info_dict)
        filter.build_basic_info()
        window.destroy()
        param_info.start_window(filename, filter)


    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    confirm_btn = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=confirm,
        relief="flat"
    )
    confirm_btn.place(
        x=723.0,
        y=616.0,
        width=138.0,
        height=52.0
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    start_window()
