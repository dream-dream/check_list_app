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