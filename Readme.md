## 使用说明
* **编辑筛选条件**：打开工程目录下的`json`文件夹，随后：
  * 在`ErrorType.json`文件中，查看或设置需要的**筛选条件说明**。
  * 在`Condition.json`文件中，查看或设置具体筛选的参数。
  > 初始设置如下：
  > 
  > `MaxTime`：一个整数，允许用户完成问卷的最长时间（秒）
  > 
  > `MinTime`：一个整数，允许用户完成问卷的最短时间（秒）
  > 
  > `ForcedItem`：一个存储二元组的列表。规定某项问题必须选择某个回答，才被视为有效。例如，设置[4, 2]，表示编号为4的题目必须选择编号为2的选项，才能通过。
  > 
  > `RepeatItem`：一个存储二元组的列表。规定两道重复的题目必须选择相同的回答，才被视为有效。例如，设置[1, 6]，表示编号为1和6的题目，必须选择一样的选项，才能通过。
  > 
  > `SamePercent`：一个不大于1的浮点数。规定用户作答结果中，相同选项的重复率的最大值。
* **准备原数据**：将原始问卷结果表格文件(.xlsx)放入根目录的`Source`文件夹下。
* **进行筛选**：打开`Main.py`，并运行。结果文件会保存在根目录的`Result`文件夹下。包括三个.xlsx文件：原始表格、筛选后的表格，以及数据筛选统计报告。

## 输出文件说明
程序会输出三个文件：原始表格、筛选后的表格，以及数据筛选统计报告。前两者容易理解，现对**数据筛选统计报告**的内容进行解说：
* 表格第一行是**原问卷数据的行数（问卷份数）**，第二行是**筛选过后数据的行数**。
* 第三行是**根据筛选条件判断为无效的问卷份数** ，后面紧跟着这条记录的**序号**（表格第一列）。
* 下面，每行展示了每个筛选条件分别筛掉了多少份问卷，并展示它们的**序号**。

## 拓展性说明
* 若要增加新的筛选条件，则必须同步修改`json`文件夹下的两个文件，并且确保`ErrorType`中的每个错误类型，都能按顺序对应至`Condition`中的条件参数配置项。
* 增加新的筛选条件后，需要修改`Filter.py`中，类`Filter`的`process()`方法，在这里书写新的判断逻辑；同时还需要修改`DeleteRecord.py`中，对于类变量`record`的初始化定义，需要确保按照`json/ErrorType`中的顺序。
> **例**：现在有5个筛选条件类型存储于`ErrorType.json`中，按数组顺序编号为0 ~ 4；那么在`DeleteRecord`中，类变量`record[0] ~ record[4]`就需要一一对应编号0 ~ 4的这五个筛选条件类型。
* 由于问卷并不是每个题目都会作为筛选，像姓名、性别、年龄这种题目肯定是不参与筛选的，并且要筛选的题目数量也会变化，因此当前程序只适配这份问卷的格式。要适配所有格式，还需要记录哪些问题是要参与筛选的。（这一点主要体现在”选择过于集中“这个筛选条件的判断上）
