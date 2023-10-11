# 将问卷中的使用时间转换成秒数
def to_second(time_str: str):
    if '时' not in time_str:  # 没有小时
        return to_second_only_minute(time_str)
    else:  # 有小时（但是示例数据中并没有这种情况）
        hour_idx = time_str.index('时')
        seconds = int(time_str[0:hour_idx]) * 3600
        # 再用同样逻辑判断分钟和秒
        seconds += to_second_only_minute(time_str, hour_idx + 1)
        return seconds


# 仅限转换分钟和秒
def to_second_only_minute(time_str, start_idx=0):
    # 判断是否有下标越界
    if start_idx >= len(time_str):
        return 0
    if time_str[-1] == '秒':
        if '分' not in time_str:
            return int(time_str[start_idx:-1])
        else:
            min_idx = time_str.index('分')
            return int(time_str[start_idx:min_idx]) * 60 + int(time_str[(min_idx + 1):-1])
    else:
        return int(time_str[start_idx:-1]) * 60


if __name__ == '__main__':
    print(to_second("1时10分"))
    print(to_second("2分30秒"))
    print(to_second("1时12秒"))
    print(to_second("3时"))
    print(to_second("40分"))
    print(to_second("19秒"))
