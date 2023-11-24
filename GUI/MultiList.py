import tkinter as tk
from tkinter import font


def on_confirm():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(index) for index in selected_indices]
    print("选中的下标:", [index for index in selected_indices])
    print("选中的项:", selected_items)
    root.destroy()


def invert_selection():
    all_items = range(listbox.size())
    selected_indices = listbox.curselection()
    for i in all_items:
        if i in selected_indices:
            listbox.selection_clear(i)
        else:
            listbox.select_set(i)


def print_selected_items():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(index) for index in selected_indices]
    print("已选中的项:", selected_items)


root = tk.Tk()
root.title("可滚动列表窗口")

listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for i in range(50):
    listbox.insert(tk.END, f"项 {i}")

scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
listbox.configure(yscrollcommand=scrollbar.set)

select_all_button = tk.Button(root, text="全选", command=lambda: listbox.select_set(0, tk.END))
select_all_button.pack(side=tk.BOTTOM, padx=5)

invert_selection_button = tk.Button(root, text="反选", command=invert_selection)
invert_selection_button.pack(side=tk.BOTTOM, padx=5)

print_selected_button = tk.Button(root, text="打印已选中项", command=print_selected_items)
print_selected_button.pack(side=tk.BOTTOM, padx=5)

confirm_button = tk.Button(root, text="确认", command=on_confirm, width=10, height=2)
confirm_button.pack(side=tk.BOTTOM, padx=5, pady=5)

text = tk.Text(root, width=30)
text.pack(side=tk.RIGHT)
text.insert(tk.END, "提示：\n本页面中，请在左侧列表中找到要参与筛选的问题，并选中。列表是按照原问卷的问题列顺序来排列的。当一项为高亮显示，则说明其已经被选中。\n"
                    "为提高操作速度，该页面支持多种便捷操作：\n"
                    " 1. 你可以像在资源管理器中选择文件一样，按住Ctrl键多选，或是按Shift选中开头至结尾之间的所有项；\n"
                    " 2. 你可以鼠标左键，光标在左侧一项上按住并上下滑动。你鼠标所经过的项全部都会被选中。类似地，若你同时按住Ctrl，则进行下一次滑动选择时，上一次被选中的项目仍然会保留。\n"
                    " 3. 你可以使用右侧的“全选”和“反选”按钮，来快速进行选择。\n\n"
                    "当选择完成后，可以单击“确认”，保存结果并返回上个页面。")
text.config(font=font.Font(family="Microsoft Yahei", size=12))

root.mainloop()
