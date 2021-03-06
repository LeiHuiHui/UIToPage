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

def get_preprocessed_img(img_path, image_size):
    import cv2
    img = cv2.imread(img_path)
    img = cv2.resize(img, (image_size, image_size))
    img = img.astype('float32')
    # Normalize image to between 0 and 255
    img /= 255
    return img

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
        print("初始化model...")
        self.model = newpix2code(self.input_shape, self.output_size, self.trained_model_path, self.vocabulary_size)
        print("初始化sampler...")
        self.sampler = Sampler(self.trained_model_path, self.input_shape, self.output_size, CONTEXT_LENGTH)
        print("初始化compiler...")
        self.compiler = Compiler(self.dsl_path)
        print("载入weights...")
        self.model.load(name=self.trained_model_name, weights_name=self.trained_weights_file)

    def loadUI(self,ui_image_path):
        # 从路径中读取图片，并预处理成模型需要的大小
        file_name = basename(ui_image_path)[:basename(ui_image_path).find(".")]
        evaluation_img = get_preprocessed_img(ui_image_path, IMAGE_SIZE)
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
        result = result.replace("{","{\n").replace("}","\n}\n")
        result = result.replace("\n\n","\n").replace("\n{}".format(END_TOKEN),END_TOKEN)
        gui = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
        gui_file_path = "{}{}.gui".format(output_path, file_name)
        with open(gui_file_path, 'w') as out_f:
            out_f.write(gui)
        return gui_file_path,gui

    def get_html(self, gui_file, gui):
        # 调用模型compiler，得到UI对应的html代码
        file_uid = basename(gui_file)[:basename(gui_file).find(".")]
        path = gui_file[:gui_file.find(file_uid)]

        input_file_path = "{}{}.gui".format(path, file_uid)
        output_file_path = "{}{}.html".format(path, file_uid)
        tokens = gui
        print("get tokens:",tokens)
        print("output html file path:",output_file_path)
        self.compiler.compile_p2c(input_file_path, output_file_path, rendering_function=render_content_with_text)
        # self.compiler.compile(tokens,output_file_path)
        return output_file_path
