import os

ATTR_FOR_PARSE = "layout-name"
CURRENT_PATH = os.path.abspath(__file__)
# print('current_path:', CURRENT_PATH)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
# print('father_path:',FATHER_PATH)
ROOT_PATH = os.path.abspath(os.path.dirname(FATHER_PATH))
# print('root_path',ROOT_PATH) 
# */UIToPage/flask_server
JSON_PATH = FATHER_PATH + "/components.json"
# 文件存放路径
DATA_FOLDER = ROOT_PATH + "/data/"

TRAINED_MODEL_FOLDER = ROOT_PATH + "/recongnizeBootstrap/trained_model/"
TRAINED_WEIGHTS_FILE = "weight.h5"
TRAINED_MODEL_NAME = "newpix2code"
DSL_PATH = ROOT_PATH + "/recongnizeBootstrap/compiler/assets/web-dsl-mapping.json"