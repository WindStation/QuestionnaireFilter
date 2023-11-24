import tkinter as tk
from tkinter import ttk


def delete_row():
    selected_item = table.selection()
    if selected_item:
        table.delete(selected_item)


def confirm():
    data = []
    for item_id in table.get_children():
        values = table.item(item_id, 'values')
        data.append([values[0], values[1]])
    print("表格内容:", data)


root = tk.Tk()
root.title("可编辑表格窗口")

left_outer = tk.Frame(root)
left_upper = tk.Frame(left_outer)
left_down = tk.Frame(left_outer)

left_outer.pack(side=tk.LEFT)
left_upper.pack(side=tk.TOP)
left_down.pack(side=tk.BOTTOM)

# 创建Treeview表格
table = ttk.Treeview(left_upper, columns=("Column 1", "Column 2"), show="headings", height=5)
table.heading("Column 1", text="下拉框")
table.heading("Column 2", text="用户输入框")
table.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

scrollbar = tk.Scrollbar(left_upper, command=table.yview())
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
table.configure(yscrollcommand=scrollbar.set)

# 添加下拉框列
table.column("Column 1", width=150, anchor="center")
table.column("Column 2", width=150, anchor="center")

# 添加下拉框到表格的第一列
combo_values = ["选项1", "选项2", "选项3"]
# table.insert("", tk.END, values=(combo_values[0], ""))

# 添加Combobox和Entry
table_combobox = ttk.Combobox(left_down, values=combo_values)
table_combobox.pack(side=tk.LEFT, padx=5)

textvar = tk.StringVar()
textvar.trace("w", lambda *args: onchange())

table_entry = ttk.Entry(left_down, textvariable=textvar)
table_entry.pack(side=tk.LEFT, padx=5)


def onchange():
    print(textvar.get())


def add_row():
    table.insert("", tk.END, values=(table_combobox.current(), table_entry.get()))


# 添加按钮
add_button = tk.Button(root, text="增加", command=add_row)
add_button.pack(side=tk.BOTTOM, padx=5)

delete_button = tk.Button(root, text="删除", command=delete_row)
delete_button.pack(side=tk.BOTTOM, padx=5)

confirm_button = tk.Button(root, text="确认", command=confirm)
confirm_button.pack(side=tk.BOTTOM, padx=5)

# 加一个文本框
text = tk.Text(root)
text.insert(tk.END, "说明")
text.pack(side=tk.RIGHT)

root.mainloop()
