import datetime
import random
import os
import json
import re
from assets.Utils import *
from assets.Config import *

CURRENT_PATH = os.path.abspath(__file__)
# print('current_path:', CURRENT_PATH)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
# print('father_path:',FATHER_PATH)


# 生成唯一的文件名，避免重复
class Pic_str:
    def create_uuid(self):  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum


class UIRecongnizer:
    def __init__(self, ui_image_path):
        self.model_name = "UItoPage"
        self.ui_image_path = ui_image_path
        self.gui = ""
        self.html = ""

    def loadUI(self):
        # 从路径中读取图片，并预处理成模型需要的大小
        return 0

    def get_gui(self):
        # 加载模型， 并调用模型sampler，得到UI对应的gui
        return 0

    def get_html(self):
        # 调用模型compiler，得到UI对应的html代码
        return 0

    def parse_html(self):
        # 取生成的HTML的container，并转换成应用需要的draggable_components
        # 以page-2576.html为例
        test_html_path = ROOT_PATH+"/page-2576.html"
        soup = make_soup(test_html_path)

        # 读取 components.json,此文件需保持最新
        jsonfile = open(JSON_PATH, 'r', encoding='utf-8')
        jsoncontent = jsonfile.read()
        # print(jsoncontent)
        jsonfile.close()
        components_dict = json.loads(jsoncontent)

        # 定位<main>
        main = soup.main
        # print(body)
        # container = body.find(attrs={"class": "container"})
        component_num = 0
        tag = main.find(attrs={"%s" % (ATTR_FOR_PARSE): re.compile(r".")})
        # 遍历main下的元素
        while tag is not None:
            component_name = tag.attrs["%s" % (ATTR_FOR_PARSE)]
            # 从json文件中获取新的替换它的代码
            component_operation = components_dict["%s" %
                                                component_name]["component_operation"]
            component_code = components_dict["%s" %
                                            component_name]["component_code"]
            print("Get a layout component:", tag.attrs["%s" % (ATTR_FOR_PARSE)])
            # print("component operations:",component_operation)
            # print("component code:",component_code)
            print("Get component operations")

            # 定位父元素
            tag_parent = tag.parent
            # 首先将tag从它的父元素移除，存入component_pure中
            # component_pure = tag.extract()
            # 保存当前tag的所有子元素
            # tag_child_list = [tag for tag in tag.contents]
            # print(type(component_operation))
            component_operation = BeautifulSoup(component_operation, "html.parser")
            # print(component_operation)
            component_wrap = component_operation.find(
                attrs={"component-name": re.compile(r".")})
            # print(component_wrap)
            # print(type(component_wrap))

            # 若使用模型的代码
            view_child = soup.new_tag("div")
            view_child["class"] = "view"
            tag.wrap(view_child)
            assert tag.parent == view_child

            view_child.wrap(component_wrap)
            assert view_child.parent == component_wrap

            '''
            # 若直接使用应用的代码
            component_code = BeautifulSoup(component_code, "html.parser")
            view_child = component_code.find(attrs={"class":"view"})
            tag.replace_with(view_child)
            view_child.wrap(component_wrap)
            print(component_wrap)
            '''

            component_num += 1
            del tag[ATTR_FOR_PARSE]
            tag = main.find(attrs={"%s" % (ATTR_FOR_PARSE): re.compile(r".")})
        print("parse %s layouts to draggable components successful!" % test_html_path)
        # print(type(main.prettify())) # 返回str
        return main.prettify()
