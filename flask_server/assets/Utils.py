from bs4 import BeautifulSoup


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
