# encoding: utf-8
import sys
import importlib

importlib.reload(sys)
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFException,PDFResourceManager, PDFPageInterpreter



def parse(path):
    fp = open(path, 'rb')
    # 用文件对象来创建一个pdf文档分析器PDFParser
    parser = PDFParser(fp)
    # 创建一个PDF文档PDFDocument
    doc = PDFDocument(parser)
    # 连接分析器 与文档对象
    parser.set_document(doc)
    # doc.set_parser(parser)
    #
    # # 提供初始化密码,如果没有密码 就创建一个空的字符串
    # doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFException
    else:
        # 创建PDf 资源管理器 来管理共享资源PDFResourceManager
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象LAParams
        laparams = LAParams()
        # 创建聚合器,用于读取文档的对象PDFPageAggregator
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象,对文档编码，解释成Python能够识别的格式：PDFPageInterpreter
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for i, page in enumerate(PDFPage.create_pages(doc)):
            # 利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page)
            # 这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象,一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal等等,想要获取文本就获得对象的text属性，
            # 参考http://www.ityouknow.com/python/2020/01/02/python-pdf-107.html
            # 使用聚合器get_result()方法获取页面内容
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    # 需要写出编码格式
                    with open(r'1.txt', 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')


if __name__ == '__main__':
    parse(path = "./pdf/江夏区乌龙泉石灰岩白云岩矿区国情调查表.pdf")