import tkinter as tk
from tkinter import ttk, font


class BasicIdQuery(tk.Toplevel):
    def __init__(self, questions, target):
        """questions: 表示所有问题的列表，按原问卷顺序"""
        super().__init__()
        self.result = None
        self.questions = questions
        self.title(target)
        self.geometry("300x200")
        self.resizable(False, False)
        self.start_window()

    def start_window(self):
        box = ttk.Combobox(self)
        value_list = [""]
        for index, question in enumerate(self.questions):
            value_list.append(question)
        box['value'] = value_list
        box.current(0)
        box.pack(pady=20)

        tk.Button(self, text="确认", command=lambda: self.ok(box), width=10, height=2).pack(pady=20)
        # confirm_btn.pack()

    def ok(self, box):
        self.result = box.get()
        self.result = self.result if self.result is not None else None
        print(box.get())
        self.destroy()


class TargetQuery(tk.Toplevel):
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.result_list = None
        self.title("请选择所有参与筛选的问题")
        self.geometry("800x600")
        self.start_window()

    def start_window(self):
        listbox = tk.Listbox(self, selectmode=tk.EXTENDED)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for index, question in enumerate(self.questions):
            listbox.insert(tk.END, f"{index}· {question}")
        # 为列表添加滚动条
        scrollbar = tk.Scrollbar(self, command=listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        listbox.configure(yscrollcommand=scrollbar.set)

        # 添加按钮
        tk.Button(self, text="确认", width=10, height=2, command=lambda: self.ok(listbox)).pack(side=tk.BOTTOM, pady=10)
        tk.Button(self, text="反选", width=10, height=2, command=lambda: self.inverse_select(listbox)).pack(side=tk.BOTTOM,
                                                                                                         pady=10)
        tk.Button(self, text="全选", width=10, height=2, command=lambda: listbox.select_set(0, tk.END)).pack(
            side=tk.BOTTOM, pady=10)

        # 说明文字
        hint = tk.Text(self, width=60)
        hint.insert(tk.END, "提示：\n本页面中，请在左侧列表中找到要参与筛选的问题，并选中。列表是按照原问卷的问题列顺序来排列的。当一项为高亮显示，则说明其已经被选中。\n"
                    "为提高操作速度，该页面支持多种便捷操作：\n"
                    " 1. 你可以像在资源管理器中选择文件一样，按住Ctrl键多选，或是按Shift选中开头至结尾之间的所有项；\n"
                    " 2. 你可以鼠标左键，光标在左侧一项上按住并上下滑动。你鼠标所经过的项全部都会被选中。类似地，若你同时按住Ctrl，则进行下一次滑动选择时，上一次被选中的项目仍然会保留。\n"
                    " 3. 你可以使用右侧的“全选”和“反选”按钮，来快速进行选择。\n\n"
                    "当选择完成后，可以单击“确认”，保存结果并返回上个页面。")
        hint.config(font=font.Font(family="Microsoft Yahei", size=12))
        hint.pack(side=tk.RIGHT)

    def inverse_select(self, listbox):
        all_items = range(listbox.size())
        selected_indices = listbox.curselection()
        for i in all_items:
            if i in selected_indices:
                listbox.selection_clear(i)
            else:
                listbox.select_set(i)

    def ok(self, listbox):
        selected_indices = listbox.curselection()
        self.result_list = [index for index in selected_indices]
        self.result_list = self.result_list if len(self.result_list) > 0 else None
        self.destroy()


if __name__ == '__main__':
    window = tk.Tk()


    def onclick():
        bid = BasicIdQuery(["1", "2", "3", "4"], target="test")
        window.wait_window(bid)


    tk.Button(window, command=onclick, text="Click").pack()

    window.mainloop()
