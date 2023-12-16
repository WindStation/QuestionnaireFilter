import tkinter as tk
from tkinter import ttk, font


class ParamForced(tk.Toplevel):
    def __init__(self, questions):
        super().__init__()
        self.result = None
        self.questions = questions
        self.title("填写强制题信息")
        self.geometry("800x500")
        self.start_window()

    def start_window(self):
        # 首先确定布局：
        # 整体分为两部分，左边left_outer，其中又有左上left_upper的表格和左下left_down的横着排列的填写框
        # 右边right_outer，其中又有右上right_upper的说明文字和右下right_down的横着排列的三个按钮
        left_outer = tk.Frame(self)
        left_upper = tk.Frame(left_outer)
        left_down = tk.Frame(left_outer)

        right_outer = tk.Frame(self)
        right_upper = tk.Frame(right_outer)
        right_down = tk.Frame(right_outer)

        left_outer.pack(side=tk.LEFT)
        left_upper.pack(side=tk.TOP)
        left_down.pack(side=tk.BOTTOM)

        right_outer.pack(side=tk.RIGHT)
        right_upper.pack(side=tk.TOP, pady=15)
        right_down.pack(side=tk.BOTTOM)

        # 创建控件
        table = ttk.Treeview(left_upper, columns=("Column 1", "Column 2"), show="headings", height=5)
        table.heading("Column 1", text="强制项（列号）")
        table.heading("Column 2", text="答案")
        table.column("Column 1", width=100, anchor=tk.CENTER)
        table.column("Column 2", width=100, anchor=tk.CENTER)
        table.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        # 给table加上滚动条
        scrollbar = tk.Scrollbar(left_upper, command=table.yview())
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        table.configure(yscrollcommand=scrollbar.set)

        # 添加选择问题和填写答案的控件
        combobox = ttk.Combobox(left_down, values=[str(i) + "· " + q for i, q in enumerate(self.questions)])
        entry = tk.Entry(left_down)
        combobox.pack(side=tk.LEFT, padx=3)
        entry.pack(side=tk.LEFT, padx=3)

        # 添加说明文字
        hint = tk.Text(right_upper, height=14)
        hint.config(font=font.Font(family="Microsoft Yahei", size=12))
        hint.insert(tk.END, "提示：\n在这个页面中，请填写所有的强制题信息。若一份作答记录中，有强制题没有选择要求的选项，则该份问卷会被视为无效。\n\n"
                            "要输入一项强制题信息，你需要在左下角先选择一道题目，并在右边的输入框中输入该题的答案，然后点击右下方的“添加”按钮。\n"
                            "在左侧上方的表格中，你可以看到已经添加的强制题序号及其选项。\n"
                            "如果发现已经输入的强制题中有错误的、或是不需要的，可以先在左侧列表中选中它，然后单击右下角的“删除”按钮。\n\n"
                            "填写完毕后，单击右下角的“确认”按钮。\n"
                            "如果没有强制题，则直接单击“确认”即可。")
        hint.pack()

        # 添加三个按钮和对应事件
        def add_row():
            table.insert("", tk.END, values=(combobox.current(), entry.get()))
            entry.delete(0, tk.END)

        def del_row():
            selected_item = table.selection()
            if selected_item:
                table.delete(selected_item)

        add_btn = tk.Button(right_down, text="添加", width=10, height=2, command=add_row, fg="#FF0000")
        del_btn = tk.Button(right_down, text="删除", width=10, height=2, command=del_row)
        ok_btn = tk.Button(right_down, text="确认", width=10, height=2, command=lambda: self.ok(table))

        add_btn.pack(side=tk.LEFT, padx=5)
        del_btn.pack(side=tk.LEFT, padx=5)
        ok_btn.pack(side=tk.LEFT, padx=5)

    def ok(self, table: ttk.Treeview):
        self.result = []
        for item_id in table.get_children():
            item = table.item(item_id, 'values')
            self.result.append([int(item[0]), item[1]])
        # print(self.result)
        self.destroy()


class ParamRepeat(tk.Toplevel):
    def __init__(self, questions):
        super().__init__()
        self.result = None
        self.questions = questions
        self.title("填写重复题信息")
        self.geometry("800x500")
        self.start_window()

    def start_window(self):
        # 整体分为两部分，左边left_outer，其中又有左上left_upper的表格和左下left_down的横着排列的填写框
        # 右边right_outer，其中又有右上right_upper的说明文字和右下right_down的横着排列的三个按钮
        left_outer = tk.Frame(self)
        left_upper = tk.Frame(left_outer)
        left_down = tk.Frame(left_outer)

        right_outer = tk.Frame(self)
        right_upper = tk.Frame(right_outer)
        right_down = tk.Frame(right_outer)

        left_outer.pack(side=tk.LEFT)
        left_upper.pack(side=tk.TOP)
        left_down.pack(side=tk.BOTTOM)

        right_outer.pack(side=tk.RIGHT)
        right_upper.pack(side=tk.TOP, pady=15)
        right_down.pack(side=tk.BOTTOM)

        # 创建控件
        table = ttk.Treeview(left_upper, columns=("Column 1", "Column 2"), show="headings", height=5)
        table.heading("Column 1", text="重复项1（列号）")
        table.heading("Column 2", text="重复项2（列号）")
        table.column("Column 1", width=100, anchor=tk.CENTER)
        table.column("Column 2", width=100, anchor=tk.CENTER)
        table.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        # 给table加上滚动条
        scrollbar = tk.Scrollbar(left_upper, command=table.yview())
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        table.configure(yscrollcommand=scrollbar.set)

        # 创建两个combobox用于选择
        combobox_1 = ttk.Combobox(left_down, values=[str(i) + "· " + q for i, q in enumerate(self.questions)])
        combobox_2 = ttk.Combobox(left_down, values=[str(i) + "· " + q for i, q in enumerate(self.questions)])
        combobox_1.pack(side=tk.LEFT, padx=3)
        combobox_2.pack(side=tk.LEFT, padx=3)

        # 说明文字
        hint = tk.Text(right_upper, height=14)
        hint.config(font=font.Font(family="Microsoft Yahei", size=12))
        hint.insert(tk.END, "提示：\n在这个页面中，请选择所有重复题。如果一份作答记录中出现了“一对重复题选择不同项”的情况，则该份作答将被视为无效。\n\n"
                            "要添加一对重复题，你需要在左下角的两个下拉框中，分别选中这对重复题。\n"
                            "在左侧的表格中，你将看到所有已经添加的重复题。\n"
                            "如果有需要删除的项，则可以在左侧表格中选中它，然后单击右下角的“删除”按钮。\n\n"
                            "全部填写好后，按“确认”按钮，保存并返回。\n"
                            "如果没有重复题，直接按“确认”即可。")
        hint.pack()

        # 三个按钮和对应事件
        def add_row():
            table.insert("", tk.END, values=(combobox_1.current(), combobox_2.current()))

        def del_row():
            selected_item = table.selection()
            if selected_item:
                table.delete(selected_item)

        add_btn = tk.Button(right_down, text="添加", width=10, height=2, command=add_row, fg="#FF0000")
        del_btn = tk.Button(right_down, text="删除", width=10, height=2, command=del_row)
        ok_btn = tk.Button(right_down, text="确认", width=10, height=2, command=lambda: self.ok(table))

        add_btn.pack(side=tk.LEFT, padx=5)
        del_btn.pack(side=tk.LEFT, padx=5)
        ok_btn.pack(side=tk.LEFT, padx=5)

    def ok(self, table):
        self.result = []
        for item_id in table.get_children():
            item = table.item(item_id, 'values')
            self.result.append([int(item[0]), int(item[1])])
        # print(self.result)
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()


    def forced_click():
        fq = ParamForced(["问题1", "问题2", "问题3"])
        root.wait_window(fq)

    def repeat_click():
        rq = ParamRepeat(["问题1", "问题2", "问题3"])
        root.wait_window(rq)

    tk.Button(root, text="ForcedTest", command=forced_click).pack()
    tk.Button(root, text="RepeatTest", command=repeat_click).pack()

    root.mainloop()
