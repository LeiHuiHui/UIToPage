import os

ATTR_FOR_PARSE = "layout-name"
CURRENT_PATH = os.path.abspath(__file__)
# print('current_path:', CURRENT_PATH)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
# print('father_path:',FATHER_PATH)
ROOT_PATH = os.path.abspath(os.path.dirname(FATHER_PATH))
# print(ROOT_PATH) */UIToPage/flask_server
JSON_PATH = FATHER_PATH + "/components.json"
