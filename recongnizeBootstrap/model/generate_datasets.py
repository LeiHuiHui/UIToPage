#!/usr/bin/env python
import os,sys
import random,math

sys.path.append("..")
from compiler.classes.Compiler import *
from compiler.classes.Utils import *

from selenium import webdriver

# generator dataset-pairs for training

DATASET_PATH = "../datasets/navbar-with-jum-dataset"
BTN_DSL_DICT = {0: "btn-red", 1: "btn-green", 2: "btn-orange", 3: "btn-blue", 4: "btn-default"}
COL_DSL_DICT = {1: "single", 2: "double", 3: "triple", 4: "quadruple"}

FORM_TYPE_DSL_DICT = {1: "form-with-icon", 2: "form-default", 3: "form-horizontal"}
INPUT_GROUP_TYPE_DICT = {0: "input-group-user", 1: "input-group-phone", 2: "input-group-lock", 3: "input-group-email", }
FORM_INPUT_TYPE_DICT = {0: "form-input-text", 1: "form-input-file"}
FORM_BUTTON_TYPE_DICT = {1: "form-btn-blue", 2: "form-btn-green", 3: "form-btn-babyblue", 4: "form-btn-default"}



def get_html_by_gui(gui, file_path, file_name, dsl_path="../compiler/assets/web-dsl-mapping.json"):
    # 将gui编译成浏览器可解析的html，默认使用web-dsl-mapping.json
    # 参考web-compiler.py

    FILL_WITH_RANDOM_TEXT = True
    TEXT_PLACE_HOLDER = "[]"

    dsl_path = "../compiler/assets/web-dsl-mapping.json"
    compiler = Compiler(dsl_path)

    def render_content_with_text(key, value):
        if FILL_WITH_RANDOM_TEXT:
            if key.find("btn") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text())
            elif key.find("title") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
            elif key.find("text") != -1:
                value = value.replace(TEXT_PLACE_HOLDER,
                                      Utils.get_random_text(length_text=56, space_number=7, with_upper_case=False))
            elif key.find("label") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
            elif key.find("checkbox") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
        return value

    input_file_path = "{}/{}.gui".format(file_path, file_name)
    output_file_path = "{}/{}.html".format(file_path, file_name)
    print(output_file_path)

    compiler.compile_p2c(input_file_path, output_file_path, rendering_function=render_content_with_text)


def get_screenshot_by_html(file_path, file_name):
    url = "{}/{}.html".format(file_path, file_name)
    picture = "{}/{}.png".format(file_path, file_name)
    browser = webdriver.PhantomJS()
    browser.get(url)
    browser.maximize_window()
    browser.save_screenshot(picture)
    browser.close()


# get_screenshot_by_html("../datasets/styles", "nav")


def save_to_gui(input_dsl, output_folder, file_name="random"):
    # 将生成的DSL code保存至.gui file
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    new_gui_file_name = ""
    if file_name == "random":
        # 将output_folder下的文件按文件名排序
        file_list = os.listdir(output_folder)
        file_nums = len(file_list)
        if file_nums == 0:
            new_gui_name = 1
        else:
            # file_list.sort()
            # new_gui_name = file_list[-1]
            # new_gui_name = str(int(new_gui_name[:new_gui_name.find(".")])+1)
            new_gui_name = str(math.ceil(file_nums/3) + 1)
        new_gui_file_name = "{}/{}.gui".format(output_folder, new_gui_name)
        while os.path.exists(new_gui_file_name):
            new_gui_name = str(int(new_gui_name) + 1)
            new_gui_file_name = "{}/{}.gui".format(output_folder, new_gui_name)
    else:
        new_gui_name = file_name
        new_gui_file_name = "{}/{}.gui".format(output_folder, new_gui_name)
        assert not os.path.exists(new_gui_file_name)
    os.mknod(new_gui_file_name)

    fp = open(new_gui_file_name, mode="w")
    fp.write(input_dsl)
    print(new_gui_file_name, "saved")
    return output_folder, new_gui_name


# new_form = random_form(form_type=3, input_text_numbers=1, input_with_label=True, has_input_file=False, has_input_checkbox=True)
# new_gui =new_form
# print(random_row(col_number=1))
# gui_file_path, gui_file_name = save_to_gui(new_gui, DATASET_PATH)
# print(get_html_by_gui(new_gui, DATASET_PATH, gui_file_name))
# get_screenshot_by_html(DATASET_PATH, gui_file_name)
# get_screenshot_by_html("./styles", "example")
# get_screenshot_by_html("../code/pix2code-bootstrap-1-code/38 train result", "794")


def generate_permutation(col_number, system):

    btn_color_permutation = []
    cur_btn_col = []
    critical = system - 1
    for j in range(col_number):
        cur_btn_col.append(0)
    # btn_color_permutation 初始化为[[0,0,0,0]]
    btn_color_permutation.append([])
    for j in range(col_number):
        btn_color_permutation[-1].append(cur_btn_col[j])

    loopornot = True
    while loopornot:
        cur = 0
        for i in range(col_number):
            if cur_btn_col[i] < critical:
                cur = i
                break
            if i == col_number-1:
                loopornot = False

        if loopornot:
            cur_btn_col[cur] += 1
            if cur > 0:
                for j in range(0,cur):
                    cur_btn_col[j] = 0
            btn_color_permutation.append([])
            for j in range(col_number):
                btn_color_permutation[-1].append(cur_btn_col[j])
    return btn_color_permutation


def random_row(col_number="random", col_types=1, btn_color="random"):
    # 栅格系统，col_number对应列数
    # 随机生成一个row
    row = "row {\n"
    if col_number == "random" and col_types == 1:
        # 表示此row只包含一种大小的col
        col_number = random.sample(range(1, len(COL_DSL_DICT)+1), 1)[0]
    print("列数：", col_number)
    if btn_color == "random":
        btn_color = random.sample(range(0, len(BTN_DSL_DICT)), col_number)
    for i in range(col_number):
        row += COL_DSL_DICT[col_number]+" {\nsmall-title, text, "+BTN_DSL_DICT[btn_color[i]]+"\n}\n"
    row += "}\n"
    return row


def generate_row_dataset(col_number):
    btn_color_permutation = generate_permutation(col_number,system=5)
    # print(random_row(col_number=col_number, btn_color=btn_color_permutation[0]))
    for i in range(len(btn_color_permutation)):
        row = random_row(col_number=col_number, btn_color=btn_color_permutation[i])
        gui_file_path, gui_file_name = save_to_gui(row, DATASET_PATH,file_name=str(155+i))
        print(get_html_by_gui(row, DATASET_PATH, gui_file_name))
        get_screenshot_by_html(DATASET_PATH, gui_file_name)

# generate_row_dataset(4)


def get_rows_from_row_file(row_files_name_list, output_file_name):
    output_file = "{}/{}.gui".format(DATASET_PATH, output_file_name)
    gui = ""

    with open(output_file, 'w') as output:
        for file_name in row_files_name_list:
            row_file = "{}/{}.gui".format(DATASET_PATH, file_name)
            row = open(row_file)
            for line in row:
                output.write(line)
                gui += line

    get_html_by_gui(gui, DATASET_PATH, output_file_name)
    get_screenshot_by_html(DATASET_PATH, output_file_name)

    print(output_file, "Done")


def generate_rows_dataset(rows, output_path=DATASET_PATH):
    row_files_list = []
    row_amount = 780
    cur_dataset_amount = int(len(os.listdir(output_path))/3)

    if rows == 2:
        for i in range(row_amount):
            row_files_list.append([i+1, i+1])
            get_rows_from_row_file([i+1, i+1], cur_dataset_amount+i+1)
    elif rows == 3:
        for i in range(row_amount):
            row_files_list.append([i+1, i+1, i+1])
            get_rows_from_row_file([i+1, i+1, i+1], cur_dataset_amount+i+1)

    for i in range(1, row_amount+1):
        if i <= 5:
            random_range = list(range(1,6))
        elif i <= 29 or i == 780:
            random_range = list(range(6,30))
            random_range.append(780)
        elif i>=30 and i<=124:
            random_range = list(range(30,125))
        else:
            random_range = list(range(125,780))
        random_range.remove(i)

        if rows == 2:
            row_files_list = [i]
            row_files_number = random.sample(random_range, 1)[0]
            row_files_list.append(row_files_number)
            get_rows_from_row_file(row_files_list, cur_dataset_amount+row_amount+i)
        if rows == 3:
            row_files_list = random.sample(random_range, rows-1)
            row_files_list.append(i)
            get_rows_from_row_file(row_files_list, cur_dataset_amount+row_amount+i)


# get_rows_from_row_file([781, 781, 781], "test")
# generate_rows_dataset(rows=2)
# generate_rows_dataset(rows=3)


def random_form(form_type="random", form_group_type_list="random", form_input_num="random", checkbox_num="random", button_type="random"):
    # 表单
    # 随机生成一个form(form-default,form-inline,form-horizontal)，默认包含button(btn-default)。
    FORM_GROUP_DSL_DICT = {1: "input-text", 2: "input-file", 3: "input-checkbox"}
    form = ""

    # add form type
    if form_type == "random":
        form_type = random.sample(range(1, 4), 1)[0]
    form_type = int(form_type)
    if form_type == 1:
        form = "form-default" + " {\n"
    else:
        form = FORM_TYPE_DSL_DICT[form_type]+" {\n"

    if form_type == 1:
        # add form_group
        if form_group_type_list == "random":
            input_number = random.sample(range(1, 5), 1)[0]
            form_group_type_list = random.sample(range(0, len(INPUT_GROUP_TYPE_DICT)), input_number)
        for input_group_type in form_group_type_list:
            input_group_type = int(input_group_type)
            form_group = "form-group {\n" + INPUT_GROUP_TYPE_DICT[input_group_type] + "\n}\n"
            form += form_group
    elif form_type == 2:
        # add form_group
        if form_group_type_list == "random":
            input_number = random.sample(range(1, 5), 1)[0]
            form_group_type_list = random.sample(range(0, len(INPUT_GROUP_TYPE_DICT)), input_number)
        for form_input_type in form_group_type_list:
            form_input_type = int(form_input_type)
            form_group = "form-group {\n" + FORM_INPUT_TYPE_DICT[form_input_type] + "\n}\n"
            form += form_group
        # add checkbox
        if checkbox_num:
            if checkbox_num == "random":
                checkbox_num = random.sample(range(0, 5), 1)[0]
            checkbox_num = int(checkbox_num)
            form += "form-group {\n"
            for i in range(checkbox_num):
                form += "form-input-checkbox"
                if i < checkbox_num-1:
                    form += ", "
            form += "\n}\n"
    elif form_type == 3:
        # add form_group
        if form_input_num == "random":
            form_input_num = random.sample(range(1, 11), 1)[0]
        form_input_num = int(form_input_num)
        for i in range(form_input_num):
            form += "form-group {\n" + "form-input-horizontal" + "\n}\n"
        # add checkbox
        if checkbox_num:
            if checkbox_num == "random":
                checkbox_num = random.sample(range(0, 4), 1)[0]
            checkbox_num = int(checkbox_num)
            form += "form-group {\nform-group-horizontal {\n"
            for i in range(checkbox_num):
                form += "form-input-checkbox"
                if i < checkbox_num - 1:
                    form += ", "
            form += "\n}\n}\n"
    # add button
    if button_type:
        if button_type == "random":
            button_type = random.sample(range(1, len(FORM_BUTTON_TYPE_DICT)+1), 1)[0]
        button_type = int(button_type)
        if form_type == 3:
            form_btn = "form-group {\nform-group-horizontal {\n" + BTN_DSL_DICT[button_type-1] + "\n}\n}\n"
        else:
            if button_type <= len(FORM_BUTTON_TYPE_DICT):
                form_btn = "form-group {\n" + FORM_BUTTON_TYPE_DICT[button_type] + "\n}\n"
            else:
                form_btn = "form-group {\n" + BTN_DSL_DICT[button_type-len(FORM_BUTTON_TYPE_DICT)-1] + "\n}\n"
        form += form_btn

    # if has_input_file:
    #     form += "form-group {\nlabel, input-file\n}"
    #     form += "\n"
    # if has_input_checkbox:
    #     form += "checkbox {\ninput-checkbox\n}"
    #     form += "\n"
    # if has_button:
    #     btn_type = random.sample(range(0, 5), 1)[0]
    #     if form_type == 3:
    #         form += "form-group {\n" + BTN_DSL_DICT[btn_type]+"\n}\n"
    #     else:
    #         form += BTN_DSL_DICT[btn_type]+"\n"

    form += "}\n"
    return form

# print(random_form(form_type=1))


def generate_form_dataset(form_type, start_form_number, output_path=DATASET_PATH):
    form_number = start_form_number
    if form_type == 1:
        # generate forms with form_type 1
        # get input group number first
        max_input_group_num = 4
        for input_group_num in range(1, max_input_group_num+1):
            #  generate input_group_type_list of length input_group_num
            input_group_type_permu = generate_permutation(input_group_num, len(INPUT_GROUP_TYPE_DICT))
            for input_group_type_list in input_group_type_permu:
                # get btn type,0==no btn
                for btn_type in range(0, len(FORM_BUTTON_TYPE_DICT)+1):
                    new_form = random_form(form_type=1, input_group_type_list=input_group_type_list, button_type=btn_type)
                    new_form_file_name = "form-" + str(form_number)
                    # save to gui file
                    save_to_gui(new_form, output_path, file_name=new_form_file_name)
                    # get html file
                    get_html_by_gui(new_form, output_path, new_form_file_name)
                    # get screenshot
                    get_screenshot_by_html(output_path, new_form_file_name)

                    form_number += 1
    elif form_type == 2:
        # generate forms with form_type 2:form-default
        # get input group number first
        max_form_input_num = 4
        max_check_box_num = 4
        for form_input_num in range(1, max_form_input_num+1):
            #  generate input_group_type_list of length input_group_num
            form_input_type_permu = generate_permutation(form_input_num, len(FORM_INPUT_TYPE_DICT))
            for form_input_type_list in form_input_type_permu:
                # get checkbox num
                for checkbox_num in range(0, max_check_box_num+1):
                    # get btn type,0==no btn
                    for form_btn_type in range(0, len(FORM_BUTTON_TYPE_DICT)+len(BTN_DSL_DICT)+1):
                        new_form = random_form(form_type=2, form_group_type_list=form_input_type_list,
                                               checkbox_num=checkbox_num, button_type=form_btn_type)
                        new_form_file_name = "form-" + str(form_number)
                        # save to gui file
                        save_to_gui(new_form, output_path, file_name=new_form_file_name)
                        # get html file
                        get_html_by_gui(new_form, output_path, new_form_file_name)
                        # get screenshot
                        get_screenshot_by_html(output_path, new_form_file_name)

                        form_number += 1
    elif form_type == 3:
        # generate forms with form_type 2:form-default
        # get input group number first
        max_form_input_num = 10
        max_check_box_num = 3
        for form_input_num in range(1, max_form_input_num + 1):
            for checkbox_num in range(0, max_check_box_num + 1):
                for form_btn_type in range(0, len(BTN_DSL_DICT)+1):
                    new_form = random_form(form_type=3, form_input_num=form_input_num, checkbox_num=checkbox_num, button_type=form_btn_type)
                    new_form_file_name = "form-" + str(form_number)
                    # save to gui file
                    save_to_gui(new_form, output_path, file_name=new_form_file_name)
                    # get html file
                    get_html_by_gui(new_form, output_path, new_form_file_name)
                    # get screenshot
                    get_screenshot_by_html(output_path, new_form_file_name)

                    form_number += 1
    return form_number

# generate_form_dataset(form_type=3, start_form_number=3200)

NAVBAR_TYPE_DICT = {0: "navbar-default", 1:"navbar-inverse"}
NAVBAR_LI_TYPE_DICT = {0: "ul-li-default", 1: "ul-li-dropout"}


def random_navbar(li_type_list=[], navbar_type="random"):
    nav = ""
    # add navbar_type
    if navbar_type == "random":
        navbar_type = random.sample(len(NAVBAR_TYPE_DICT), 1)[0]
    navbar_type = int(navbar_type)
    nav += NAVBAR_TYPE_DICT[navbar_type] + "{\n"

    # add nav-ul left
    if len(li_type_list):
        # add navbar-collapse
        nav += "div-navbar-collapse {\n"
        # print(li_type_list)
        nav += "ul-navbar-nav {\n"
        i = 0
        for li_type in li_type_list:
            nav += NAVBAR_LI_TYPE_DICT[li_type]
            if i != len(li_type_list)-1:
                nav += ", "
            i += 1
        nav += "\n}\n}\n"
    nav += "}\n"
    return nav


def generate_navbar_dataset(start_navbar_number=0, output_path=DATASET_PATH):
    navbar_number = start_navbar_number
    max_navbar_li = 9

    # navbar-default or navbar-inverse
    for navbar_type in range(len(NAVBAR_TYPE_DICT)):
        # has navbar-left
        for navbar_left_li_num in range(1, max_navbar_li+1):
            # get li_type list
            li_left_type_permu = generate_permutation(navbar_left_li_num, len(NAVBAR_LI_TYPE_DICT))
            for li_left_type_list in li_left_type_permu:
                # print(li_left_type_list)
                new_navbar = random_navbar(navbar_type=1, li_type_list=li_left_type_list)
                new_navbar_file_name = "navbar-" + str(navbar_number)
                # save to gui file
                save_to_gui(new_navbar, output_path, file_name=new_navbar_file_name)
                # get html file
                get_html_by_gui(new_navbar, output_path, new_navbar_file_name)
                # get screenshot
                get_screenshot_by_html(output_path, new_navbar_file_name)
                navbar_number += 1
    return navbar_number

# generate_navbar_dataset(start_navbar_number=1023)


def generate_navbar_with_jum_dataset(navbar_file_path, output_path):
    for f in os.listdir(navbar_file_path):
        if f.find(".gui") != -1:
            # f is like "navbar-8.gui"
            jum_file_number = f[7:f.find(".gui")]
            jum_file_name = "navjum-"+jum_file_number
            jum_file = "{}/{}.gui".format(output_path, jum_file_name)

            with open(jum_file, 'w') as output:
                navbar_gui = open("{}/{}".format(navbar_file_path, f))
                navbar_gui = navbar_gui.read()
                new_gui = navbar_gui + "jumbotron {\nh1, text\n}\n"
                # print(gui)
                # for line in navbar_gui:
                #     output.write(line)
                output.write(new_gui)
            get_html_by_gui(new_gui, output_path, jum_file_name)
            get_screenshot_by_html(output_path, jum_file_name)

# generate_navbar_with_jum_dataset(navbar_file_path="../datasets/navbar-dataset", output_path=DATASET_PATH)


def generate_page_dataset(nav_file_path="../datasets/navbar-with-jum-dataset",
                          rows_file_path="../datasets/rows-dataset", output_path="../datasets/page-dataset"):
    nav_files = os.listdir(nav_file_path)
    rows_files = os.listdir(rows_file_path)
    page_number = 1
    for i in range(1, 3900+1):
        rows_file = "{}/{}.gui".format(rows_file_path, str(i))
        if i <= 2044:
            # nav_file = "{}/{}.gui".format(nav_file_path, "navjum-"+str(i))
            page_number += 1
            continue
        elif i <= 2972:
            nav_file = "{}/{}.gui".format(nav_file_path, "navjum-"+str(i-1950))
        else:
            nav_file = "{}/{}.gui".format(nav_file_path, "navjum-"+str(i-1856))
        rows = open(rows_file).read()
        nav = open(nav_file).read()
        page_file_name = "page-" + str(page_number)
        page_file = "{}/{}.gui".format(output_path, page_file_name)
        if not os.path.exists(page_file):
            os.mknod(page_file)
        with open(page_file,'w') as output:
            output.write(nav)
            output.write(rows)

        page_gui = nav + rows
        # print(page_gui)
        get_html_by_gui(page_gui, output_path, page_file_name)
        get_screenshot_by_html(output_path, page_file_name)
        page_number += 1
generate_page_dataset()



