# -*- coding: utf-8 -*-


import jpype

# 路径
jvmPath = jpype.getDefaultJVMPath()  # 获得系统的jvm路径
WORK_DIR = "/Users/jiecai/PycharmProjects/矿产文件识别/"
ext_classpath = f"{WORK_DIR}ner/hanlp/hanlp-1.8.2.jar:{WORK_DIR}ner/hanlp"
jvmArg = '-Djava.class.path=' + ext_classpath
jpype.startJVM(jvmPath, jvmArg, "-Xms1g", "-Xmx1g")


# 繁体转简体
def TraditionalChinese2SimplifiedChinese(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    return HanLP.convertToSimplifiedChinese(sentence_str)


# 切词&命名实体识别与词性标注(可以粗略识别)
def NLP_tokenizer(sentence_str):
    NLPTokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
    return NLPTokenizer.segment(sentence_str)


# 地名识别，标注为ns
def Place_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enablePlaceRecognize(True)
    # segment = HanLP.newSegment().enableAllNamedEntityRecognize(True)

    return HanLP.segment(sentence_str)


# 人名识别,标注为nr
def PersonName_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enableNameRecognize(True)
    return HanLP.segment(sentence_str)


# 机构名识别,标注为nt
def Organization_Recognize(sentence_str):
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    segment = HanLP.newSegment().enableOrganizationRecognize(True)
    return HanLP.segment(sentence_str)


# 标注结果转化成列表
def total_result(function_result_input):
    x = str(function_result_input)
    y = x[1:len(x) - 1]
    y = y.split(',')
    return y


# 时间实体
def time_result(total_result):
    z = []
    for i in range(len(total_result)):
        if total_result[i][-2:] == '/t':
            z.append(total_result[i])
    return z


# Type_Recognition 可以选 ‘place’,‘person’,‘organization’三种实体,
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


# 把单一实体结果汇总成一个字典
def ner_dict_result(sentence_str):
    sentence = TraditionalChinese2SimplifiedChinese(sentence_str)
    print(sentence)
    total_dict = {}
    a = total_result(Place_Recognize(sentence))
    print(a)
    b = single_result('place', a)
    c = total_result(PersonName_Recognize(sentence))
    d = single_result('person', c)
    e = total_result(Organization_Recognize(sentence))
    f = single_result('organization', e)
    g = total_result(NLP_tokenizer(sentence))
    h = time_result(g)
    total_list = [i for i in [b, d, f, h]]
    total_dict.update(place=total_list[0], person=total_list[1], organization=total_list[2], time=total_list[3])
    # jpype.shutdownJVM()  # 关闭JVM虚拟机
    return total_dict


# # 测试
# test_sentence = "本次调查工作，首先收集了省牵头单位提供的2019年矿产资源利用现状调查资料，然后从省地质资料收集到矿区最新地质报告、储量核实报告等，同时收集了武汉市江夏区矿产资源管理总站乌龙泉矿2019年储量矿山储量数据新老转换的成果、乌龙泉矿2020年储量年报，再就是积极和矿山联系，收集到了矿山最新的采矿证，最新的开发利用方案、占用矿产资源储量登记书、企业信息公示（2019、2020），些外还有测量控制点成果表、矿山成品矿生产报表2020、成品矿生产报表2021、生产报表2020、生产报表2021等资料。"
# print(ner_dict_result(test_sentence))

