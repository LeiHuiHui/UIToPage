import os
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver

CURRENT_PATH = os.path.abspath(__file__)
print('current_path:', CURRENT_PATH)
FATHER_PATH = os.path.abspath(os.path.dirname(CURRENT_PATH))
print('father_path:',FATHER_PATH)


def matlabPic():
    history={"val_acc":[0.8938,0.9079,0.9233,0.9333,0.9392,0.9432,0.9505,0.9454,0.9456,0.9428],"loss":[0.7229,0.2070,0.1744,0.1550,0.1436,0.1329,0.1265,0.1217,0.1179,0.1129]}

    real_epoches = 10
    # plt.style.use("ggplot")
    plt.figure(0)  # 可以自定义图片大小和颜色等
    # 绘制训练损失值
    plt.plot(np.arange(1, real_epoches+1), history['loss'], label="train_loss")
    plt.title('Train loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    # plt.show()
    plt.savefig("train_loss_1.png")
    plt.close(0)

    plt.figure(0)  # 可以自定义图片大小和颜色等
    plt.plot(np.arange(1, real_epoches+1), history['val_acc'], label="val_acc")
    plt.title('Validation accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    # plt.legend(['Train'], loc='upper left')
    plt.legend(loc='lower right')
    # plt.show()
    plt.savefig("val_acc_1.png")
    plt.close(0)

    plt.figure(0)  # 可以自定义图片大小和颜色等
    # 绘制训练损失值 & 验证准确率值
    plt.plot(np.arange(1, real_epoches+1), history['loss'], label="train_loss")
    plt.plot(np.arange(1, real_epoches+1), history['val_acc'], label="val_acc")
    plt.title('Train loss&Val acc')
    plt.ylabel('Loss&Acc')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    # plt.show()
    plt.savefig("train_loss and eval_acc_1.png")
    plt.close(0)

def get_screenshot_by_html(file_path, file_name):
    url = "{}/{}.html".format(file_path, file_name)
    picture = "{}/{}-html.png".format(file_path, file_name)
    browser = webdriver.PhantomJS()
    browser.get(url)
    browser.maximize_window()
    browser.save_screenshot(picture)
    browser.close()
    print(picture ,"saved")

get_screenshot_by_html(FATHER_PATH,"form-3041 (1)")
get_screenshot_by_html(FATHER_PATH,"form-3262")
get_screenshot_by_html(FATHER_PATH,"page-2576")
get_screenshot_by_html(FATHER_PATH,"page-3850")
