import requests
import json
# from pyhanlp import *
from jpype import JClass
content = (
    "程序员(英文Programmer)是从事程序开发、维护的专业人员。"
    "一般将程序员分为程序设计人员和程序编码人员，"
    "但两者的界限并不非常清楚，特别是在中国。"
    "软件从业人员分为初级程序员、高级程序员、系统"
    "分析员和项目经理四大类。")
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")

HanLP = JClass('com.hankcs.hanlp.HanLP')

def get_keywords_aminer(text):
    # 指定请求参数格式为json
    request_url = "http://nlpapi.aminer.cn/word_cut/keywords"
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": text
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        return response.json()['data']


def get_keywords_hanlp(text):
    keyword_list = HanLP.extractKeyword(text, 10)
    return keyword_list


def get_summary_hanlp(text):
    summary_list = HanLP.extractSummary(text, 3)
    return summary_list


def get_phrase_hanlp(text):
    phrase_list = HanLP.extractPhrase(text, 10)
    return phrase_list
