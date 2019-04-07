import datetime
import random
import json
import re
import sys
from bs4 import BeautifulSoup
from os.path import basename
from recongnizeBootstrap.model.classes.Sampler import *
from recongnizeBootstrap.model.classes.model.newpix2code import *
from recongnizeBootstrap.compiler.classes.Utils import *
from recongnizeBootstrap.compiler.classes.Compiler import *

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
    def __init__(self,trained_model_path,trained_weights_file,trained_model_name,dsl_path):
        self.trained_model_path = trained_model_path
        self.trained_model_name = trained_model_name
        self.trained_weights_file = trained_weights_file
        self.dsl_path = dsl_path
        # self.ui_image_path = ""
        # self.output_path = ""
        self.search_method = "greedy"
        self.model = None
        self.sampler = None
        self.compiler = None

    def initialRecongnizer(self):
        # 加载模型
        meta_dataset = np.load("{}/meta_dataset.npy".format(self.trained_model_path))
        self.input_shape = meta_dataset[0]
        self.output_size = meta_dataset[1]
        self.vocabulary_size = meta_dataset[2]
        self.model = newpix2code(input_shape, output_size, self.trained_model_path, vocabulary_size)
        self.model.load(name=self.trained_model_name, weights_name=self.trained_weights_file)
        self.sampler = Sampler(self.trained_model_path, self.input_shape, self.output_size, CONTEXT_LENGTH)
        self.compiler = Compiler(dsl_path)

    def loadUI(self,ui_image_path):
        # 从路径中读取图片，并预处理成模型需要的大小
        file_name = basename(ui_image_path)[:basename(ui_image_path).find(".")]
        evaluation_img = Utils.get_preprocessed_img(ui_image_path, IMAGE_SIZE)
        return file_name,evaluation_img
    
    def render_content_with_text(self, key, value):
        FILL_WITH_RANDOM_TEXT = True
        TEXT_PLACE_HOLDER = "[]"
        if FILL_WITH_RANDOM_TEXT:
            if key.find("btn") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text())
            elif key.find("title") != -1:
                value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
            elif key.find("text") != -1:
                value = value.replace(TEXT_PLACE_HOLDER,
                                    Utils.get_random_text(length_text=56, space_number=7, with_upper_case=False))
        return value

    def get_gui(self, ui_image_path, output_path):
        # 调用模型sampler，得到UI对应的gui
        file_name,evaluation_img = self.loadUI(ui_image_path)
        result, _ = self.sampler.predict_greedy(self.model, np.array([evaluation_img]),require_sparse_label=False)
        print("Result greedy: {}".format(result))
        gui = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
        gui_file = "{}/{}.gui".format(output_path, file_name)
        with open(gui_file, 'w') as out_f:
            out_f.write(gui)
        return gui_file,gui

    def get_html(self, gui_file):
        # 调用模型compiler，得到UI对应的html代码
        file_uid = basename(gui_file)[:basename(gui_file).find(".")]
        path = gui_file[:gui_file.find(file_uid)]

        input_file_path = "{}{}.gui".format(path, file_uid)
        output_file_path = "{}{}.html".format(path, file_uid)
        print(output_file_path)

        self.compiler.compile_p2c(input_file_path, output_file_path, rendering_function=render_content_with_text)
        return 0
