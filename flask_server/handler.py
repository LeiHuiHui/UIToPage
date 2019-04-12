import os
from assets.Libs import *
from assets.Config import *


def get_uniq_name():
    pic_str = Pic_str()
    uniqe_name = pic_str.create_uuid()
    return uniqe_name


def save_file(file, path):
    # 保存上传的图片到本地
    uniq_name = get_uniq_name()
    file_name = file.filename
    file_type = file_name.split(".")[-1]
    ui_img_name = "{}.{}".format(uniq_name,file_type)
    img_save_path = os.path.join(path,ui_img_name)
    file.save(img_save_path)
    while os.access(img_save_path,os.R_OK) and os.path.getsize(img_save_path)>0:
        print("接收UI image，保存至",img_save_path)
        break
    return img_save_path

def sample_ui_to_html_withoutInitial(recognizer,img_path,output_path):
    '''
    img_path:UI img的绝对路径
    '''
    gui_file_path, result_gui = recognizer.get_gui(img_path,output_path)
    html_file_path = recognizer.get_html(gui_file_path, result_gui)
    return html_file_path

def sample_ui_to_html(img_path,output_path):
    '''
    img_path:UI img的绝对路径
    '''
    recognizer = None
    recognizer = UIRecongnizer(TRAINED_MODEL_FOLDER,TRAINED_WEIGHTS_FILE,TRAINED_MODEL_NAME,DSL_PATH)
    recognizer.initialRecongnizer()
    gui_file_path, result_gui = recognizer.get_gui(img_path,output_path)
    html_file_path = recognizer.get_html(gui_file_path, result_gui)
    return html_file_path

def parse_html(html_file_path):
        # 取生成的HTML的container，并转换成应用需要的draggable_components
        # 以page-2576.html为例
        # test_html_path = ROOT_PATH+"/page-2576.html"
        soup = make_soup(html_file_path)

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
        print("parse %s layouts to draggable components successful!" % html_file_path)
        # print(type(main.prettify())) # 返回str
        return main.prettify()