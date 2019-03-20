import time


def get_gender(arg):
    li_gender = ["female", "male"]
    for item_gender in li_gender:
        if arg == item_gender:
            return li_gender.index(arg)


def get_salary(arg):
    li_salary = ["<2000", '2000-5000', '5000-8000', '8000-10000', '10000<']
    for item_salary in li_salary:
        if arg == item_salary:
            return li_salary.index(arg)


def get_time_format(arg):
    """
    时间格式转换
    :param arg: 时间字符串
    :return: 时间戳
    """
    try:
        format_time_str = time.strptime(arg, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        struct_time = time.strptime(arg, "%Y-%m-%d")
        return time.mktime(struct_time)
    return time.mktime(format_time_str)

str = "2019-01-12 21:23:12"
# struct_time = time.strptime(str, "%Y-%m-%d")
print(get_time_format(str))