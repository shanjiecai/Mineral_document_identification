from pyhanlp import *
import zipfile
import os
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH
import jieba
import re
from string import digits


def test_data_path():
    """
    获取测试数据路径，位于$root/data/test，根目录由配置文件指定。
    :return:
    """
    data_path = os.path.join(HANLP_DATA_PATH, 'test')
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    return data_path


# 获取中文字符
def get_chinese(text):
    pre = re.compile(u'[\u4e00-\u9fa5]')
    res = re.findall(pre, text)
    res1 = ''.join(res)
    return res1


# 文本清洗
def clean_text(text):
    # 需要自定义在医疗政策领域的词典
    wordlist = jieba.cut(text)
    # 去除停用词和长度小于2的词语
    wordlist = [w for w in wordlist if w not in stopwords and len(w) > 1]
    # 将中文数据组织成类似西方于洋那样，词语之间以空格间隔
    document =  "".join(wordlist)
    return document


def read_stopwords():
    # stopword_files = [
    #     'baidu_stopwords.txt', 'cn_stopwords.txt', 'hit_stopwords.txt',
    #     'my_stopwords.txt', 'scu_stopwords.txt', 'more_stopwords.txt'
    # ]
    stopword_files = ['stopword1.txt','stopword2.txt']
    stopwords_list = []
    for stopwords in stopword_files:
        f = open('./stopwords/' + stopwords, encoding='utf-8')
        for l in f.readlines():
            stopwords_list.append(l.strip())
    return stopwords_list


## 验证是否存在 MSR语料库，如果没有自动下载
def ensure_data(data_name, data_url):
    root_path = test_data_path()
    dest_path = os.path.join(root_path, data_name)
    if os.path.exists(dest_path):
        return dest_path

    if data_url.endswith('.zip'):
        dest_path += '.zip'
    download(data_url, dest_path)
    if data_url.endswith('.zip'):
        with zipfile.ZipFile(dest_path, "r") as archive:
            archive.extractall(root_path)
        remove_file(dest_path)
        dest_path = dest_path[:-len('.zip')]
    return dest_path


## 指定 PKU 语料库
PKU98 = ensure_data("pku98", "http://file.hankcs.com/corpus/pku98.zip")
PKU199801 = os.path.join(PKU98, '199801.txt')
PKU199801_TRAIN = os.path.join(PKU98, '199801-train.txt')
PKU199801_TEST = os.path.join(PKU98, '199801-test.txt')
POS_MODEL = os.path.join(PKU98, 'pos.bin')
NER_MODEL = os.path.join(PKU98, 'ner.bin')

## ===============================================
## 以下开始 HMM 命名实体识别

HMMNERecognizer = JClass('com.hankcs.hanlp.model.hmm.HMMNERecognizer')
AbstractLexicalAnalyzer = JClass('com.hankcs.hanlp.tokenizer.lexical.AbstractLexicalAnalyzer')
PerceptronSegmenter = JClass('com.hankcs.hanlp.model.perceptron.PerceptronSegmenter')
PerceptronPOSTagger = JClass('com.hankcs.hanlp.model.perceptron.PerceptronPOSTagger')
Utility = JClass('com.hankcs.hanlp.model.perceptron.utility.Utility')


def train(corpus):
    recognizer = HMMNERecognizer()
    recognizer.train(corpus)  # data/test/pku98/199801-train.txt
    return recognizer


def test(recognizer, text):
    # 包装了感知机分词器和词性标注器的词法分析器
    analyzer = AbstractLexicalAnalyzer(PerceptronSegmenter(), PerceptronPOSTagger(), recognizer)
    return analyzer.analyze(text)
    # scores = Utility.evaluateNER(recognizer, PKU199801_TEST)
    # Utility.printNERScore(scores)


# 标注结果转化成列表
def total_result(function_result_input):
    x = str(function_result_input)
    y = x[1:len(x) - 1]
    y = y.split(',')
    return y


# 返回单一实体类别的列表
def single_result(Type_Recognition, total_result):
    if Type_Recognition == 'place':
        Type = '/ns'
    elif Type_Recognition == 'person':
        Type = '/nr'
    elif Type_Recognition == 'organization':
        Type = '/nt'
    else:
        print('请输入正确的参数：（place，person或organization）')
    z = []
    for i in range(len(total_result)):
        if total_result[i][-3:] == Type:
            z.append(total_result[i])
    return z


# 时间实体
def time_result(total_result):
    z = []
    for i in range(len(total_result)):
        if total_result[i][-2:] == '/t':
            z.append(total_result[i])
    return z


if __name__ == '__main__':
    # 加在停用词
    stopwords = read_stopwords()
    recognizer = train(PKU199801_TRAIN)
    text = "本次调查工作，首先收集了省牵头单位提供的2019年矿产资源利用现状调查资料，然后从省地质资料收集到矿区最新地质报告、储量核实报告等，同时收集了武汉市江夏区矿产资源管理总站乌龙泉矿2019年储量矿山储量数据新老转换的成果、乌龙泉矿2020年储量年报，再就是积极和矿山联系，收集到了矿山最新的采矿证，最新的开发利用方案、占用矿产资源储量登记书、企业信息公示（2019、2020），些外还有测量控制点成果表、矿山成品矿生产报表2020、成品矿生产报表2021、生产报表2020、生产报表2021等资料。"
    text = text.replace("[^\u4e00-\u9fa5]", "")  # 去除非汉字
    remove_digits = str.maketrans('', '', digits)  # 去除数字
    text = text.translate(remove_digits)
    text = clean_text(text)  # 分词，去除停用词
    # print(test(recognizer, "华北电力公司董事长谭旭光和秘书胡花蕊来到美国纽约现代艺术博物馆参观"))
    # print(test(recognizer, "武钢资源集团乌龙泉矿业有限公司乌龙泉矿普查找矿工作始于1953年3月，矿山1958年与武钢同步建成投产，是国有大型矿山企业，是中国宝武武汉总部唯一的冶金熔剂原料生产基地，建矿以来生产至今。"))
    total_dict = {}
    a = total_result(test(recognizer, text))
    print(a)
    for words_tag in list(a):
        print(words_tag)
        w, t = str(words_tag).rsplit('/', 1)  # 只分割最右边的/
    b = single_result('place', a)
    d = single_result('person', a)
    f = single_result('organization', a)
    h = time_result(a)
    total_list = [i for i in [b, d, f, h]]
    total_dict.update(place=total_list[0], person=total_list[1], organization=total_list[2], time=total_list[3])
    print(total_dict)
