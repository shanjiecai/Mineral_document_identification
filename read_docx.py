import re
import docx
from openpyxl import Workbook,load_workbook
from docx import Document
import requests
import json
import os
import jieba



def get_mineral_name():
    wb = load_workbook("矿产名称.xlsx")
    sheets = wb.sheetnames
    sheet = wb[sheets[0]]
    mineral_list = []
    for index,row in enumerate(sheet.rows):
        if index==0:
            continue
        # print([cell.value for cell in row])
        mineral_list.extend(cell.value for cell in row)
    return mineral_list


def get_mineral_name_simple():
    f = open("矿产名称.txt",'r',encoding="utf-8")
    mineral_list = []
    for index, row in enumerate(f.readlines()):
        # print([cell.value for cell in row])
        mineral_list.append(row.strip())
    return mineral_list

def preprocess(text):
    return text


def ner(text):
    # 指定请求参数格式为json
    request_url = "https://nlpapi.aminer.cn/ner/"
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": text
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        return response.json()['data']


def word_segment(text):
    # 指定请求参数格式为json
    request_url = "https://nlpapi.aminer.cn/word_segmentation/word_segmentation"
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": text,
        "cut_all": False,
        "HMM": True
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        # print(response.json()['data'])
        return response.json()['data']


from nltk.tokenize import RegexpTokenizer
def SplitSentence(content):
    tokenizer = RegexpTokenizer(".*?[。！？；，]") #就是以[]中的符号为标识分割的
    rst = tokenizer.tokenize(content)# list
    return rst


def read_docx(path):
    print(f"------------{path}------------")
    print("识别开始")
    document = Document(path)
    para_list = []
    para_index = 1
    for paragraph in document.paragraphs:
        mineral_tag = 0
        classify_tag = 0

        if paragraph.text.strip():
            # ner(paragraph.text.strip())
            word_segment_list = word_segment(paragraph.text.strip())
            for w in word_segment_list:
                if w in mineral_name:
                    mineral_tag=1
                if w in classify_name:
                    classify_tag=1
            if classify_tag and mineral_tag:
                print(f"第{para_index}段：", paragraph.text.strip())
                print("包含的实体为：", ner(paragraph.text.strip()))
                para_index += 1
                # sentence_list = SplitSentence(paragraph.text.strip())
                # for sent_index, sentence in enumerate(sentence_list):
                #     print(f"第{sent_index}句实体：", ner(sentence))
                para_list.append(paragraph.text.strip())
    return para_list


def recognize(text):
    # print(text)
    sentence_list = SplitSentence(text)

    result = {}
    mineral_tag = 0
    for sentence in sentence_list:
        word_segment_list = list(jieba.cut(sentence))
        # print(word_segment_list)
        for w in word_segment_list:
            if w in mineral_name:
                if w in result:
                    continue
                mineral_tag = 1
                mineral = w
                result[w] = {}
            if w in classify_name and mineral_tag:
                reg = re.compile(f"(?<={w}).*?\d+")
                match = reg.search(sentence)
                num = match.group(0)
                result[mineral][w] = num
    print("------该报告识别结果------")
    print(result)
    return result


def select_para(para_list):
    while True:
        para = input("请输入你认为准确的段落序号：(q键退出)\n")
        if para == "q":
            break
        print(para)
        recognize(para_list[int(para)-1])



if __name__ == "__main__":
    mineral_name = get_mineral_name_simple()
    classify_name = ['推断', '控制', '探明', 'TM', 'KZ', 'TD', '证实', '可信']
    tm_list = ['TM', 'tm', '探明']
    kz_list = ['KZ', 'kz', '控制']
    td_list = ['TD', 'td', '推断']
    zs_list = ['证实']
    kx_list = ['可信']
    for root, dirs, files in os.walk(r"./word"):
        path_list = []
        for file in files:
            path_list.append(os.path.join(root, file))
    # path = "./word/GQTCBG_420122402_乌龙泉矿生产矿山矿产资源国情调查报告.docx"
    for path in path_list:
        para_list = read_docx(path)
        if para_list:
            select_para(para_list)
    # recognize("调整后的保有数据为：石灰岩TM:13477千吨，KZ:16015千吨，TD:2992千吨；白云岩TM:618千吨，KZ:7374千吨，TD:0千吨。调整变化量为：石灰岩保有TM:-871千吨，KZ:-360千吨；白云岩保有TM:-551千吨，KZ:-305千吨。")
