'''
 * @Author: Hui Lei
 * @Date: 2019-03-29 22:40:55 
 * @Last Modified by: Hui Lei
 * @Last Modified time: 2019-03-29 22:46:55
 '''
import os
import re
import json
from bs4 import BeautifulSoup

attr_for_parse = "layout-name"

CURRENT_PATH = os.path.abspath(__file__)
print('current_path:', CURRENT_PATH)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
print('father_path:',FATHER_PATH)

json_path = FATHER_PATH + "/components.json"
jsonfile = open(json_path,'r',encoding='utf-8')
jsoncontent = jsonfile.read()
# print(jsoncontent)
jsonfile.close()

components_dict = json.loads(jsoncontent)
# print(type(components_dict))
# print(components_dict["12"])
def make_soup(html_file_path):
    path = html_file_path
    # 打开html文件 
    htmlfile = open(path, 'r', encoding='utf-8')
    # 读取html的句柄内容 
    htmlhandle = htmlfile.read()
    # 使用Beautifulsoup解析 
    soup = BeautifulSoup(htmlhandle, 'html.parser')
    htmlfile.close()
    return soup

def parse_html_to_traggable():
    path = FATHER_PATH+"/test/example.html"
    soup = make_soup(path)

    # 定位container
    body = soup.body
    # print(body)
    container = body.find(attrs={"class":"container"})

    component_num = 0
    tag = container.find(attrs={"%s" % (attr_for_parse): re.compile(r".")})
    # 遍历container下的元素
    while tag is not None:
        component_name = tag.attrs["%s" % (attr_for_parse)]
        # 从json文件中获取新的替换它的代码
        component_operation = components_dict["%s" % component_name]["component_operation"]
        component_code = components_dict["%s" % component_name]["component_code"]
        print("Get a layout component:",tag.attrs["%s" % (attr_for_parse)])
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
        component_operation = BeautifulSoup(component_operation,"html.parser")
        # print(component_operation)
        component_wrap = component_operation.find(attrs={"component-name":re.compile(r".")})
        # print(component_wrap)
        # print(type(component_wrap))

        # 若使用模型的代码
        view_child = soup.new_tag("div")
        view_child["class"]="view"
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

        component_num+=1
        del tag[attr_for_parse]
        tag = container.find(attrs={"%s" % (attr_for_parse): re.compile(r".")})
    print("parse %s layouts to draggable components successful!" % path)
    # print(container.prettify())
    return container


def write_to_index(parsed_container):
    '''
    参数：
    将parsed_container下的所有元素插入到index.html的demo元素下
    '''
    index_path = FATHER_PATH + "/index.html"
    ouyput_path = FATHER_PATH + "/test_index.html"
    soup = make_soup(index_path)

    demo = soup.body.find(attrs={"class":"demo ui-sortable"})
    # print(demo.prettify())
    # 首先将demo清空
    demo.string = ""

    # 将要添加的子tag保存在list components
    components = [c for c in parsed_container.contents]
    for comp in components:
        demo.append(comp)

    html = soup.prettify("utf-8")
    with open(ouyput_path,'wb') as index_file:
        index_file.write(html)
    print(html)

# 使用requests库来获取url的HTML
# import requests
# url = "http://www.baidu.com"
# try:
#     r = requests.get(url)
#     r.raise_for_status()# 如果状态不是200，引发HTTPerror异常
#     r.encoding = r.apparent_encoding
#     print(r.text[:])
# except:
#     print("failed!")

content = parse_html_to_traggable()
write_to_index(content)