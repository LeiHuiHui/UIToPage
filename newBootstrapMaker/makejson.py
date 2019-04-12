'''
 * @Author: Hui Lei 
 * @Date: 2019-03-30 20:22:04 
 * @Last Modified by:   Hui Lei
 * @Last Modified time: 2019-03-30 20:22:04 
 '''
import os
import re
import json
from bs4 import BeautifulSoup

CURRENT_PATH = os.path.abspath(__file__)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
index_path = FATHER_PATH + "/index.html"
index_file = open(index_path, "r", encoding='utf-8')
index_html = index_file.read()

soup = BeautifulSoup(index_html, "html.parser")
index_file.close()

sidebar = soup.find(attrs={"class": "sidebar-nav"})

all_components = sidebar.find_all(attrs={"component-name": re.compile(r'.')})
print("total components num:", len(all_components))

print(type(all_components))  # <class 'bs4.element.ResultSet'>
print(type(all_components[0]))  # <class 'bs4.element.Tag'>

# components_list = []
components_dict = {}

for tag in all_components:
    # get component-name
    component_name = tag["component-name"]
    # print(component_name)
    view = tag.find(attrs={"class":"view"}).extract()
    # print(view)
    # print(tag)
    component_operation = tag.prettify()
    component_code = view.prettify()
    # print(component_draggable)
    component = dict()
    component["component_code"] = component_code
    component["component_operation"] = component_operation
    components_dict["%s" % component_name] = component
# print(components_list[0])
# print(components_list[1])

# components_list.append(components_dict)
# dumps默认 encoding="utf-8"
components_json = json.dumps(components_dict)

output_path = FATHER_PATH + "/components.json"

with open(output_path, 'w') as out_f:
    out_f.write(components_json)

print("components json saved to :", output_path)