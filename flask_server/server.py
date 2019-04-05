from flask import Flask, request, Response, redirect, flash
import json
import os
from handler import *

UPLOAD_FOLDER = '/uploads'  # 文件存放路径

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


@app.route('/')
def index():
    # 这里是demo，实际这么返回响应字符串是不规范的
    return '<h1>Hello World!</h1>'

# @app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, %s!</h1>' % name


@app.route('/sample', methods=['POST'])
def sample():
    if 'ui_image' not in request.files:
        flash('No ui_image part')
        return redirect(request.url)
    file = request.files["ui_image"]  # ui_image对应表单的name属性
    file_name = file.filename
    file_tye = file_name.split(".")[-1]

    # 保存ui图至ui_img
    if file is None:
        # 表示没有发送文件
        result = {"status": 0, "info": "未上传文件"}
    else:
        pic_str = Pic_str()
        save_img_name = pic_str.create_uuid()
        ui_img = "{}.{}".format(save_img_name,file_tye)
        file.save(ui_img)
        result = {"status":1, "info":"接收到图片"+file_name}
    # 调用模型，生成tokens


    result_json = json.dumps(result)
    # Response
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(host="",port=8000,debug=True)
