import pdfplumber
import re


def pdf_tabel_func(path):
    pdf = pdfplumber.open(path)
    text = []  # 返回一个列表
    for page in pdf.pages:
        for line in page.extract_text().split("\n"):
            if line.strip():
                text.append(line.strip())
        for pdf_table in page.extract_tables():
            table = []
            cells = []
            for row in pdf_table:
                if not any(row):
                    # 如果一行全为空，则视为一条记录结束
                    if any(cells):
                        table.append(cells)
                        cells = []
                elif all(row):
                    # 如果一行全不为空，则本条为新行，上一条结束
                    if any(cells):
                        table.append(cells)
                        cells = []
                    table.append(row)
                else:
                    if len(cells) == 0:
                        cells = row
                    else:
                        for i in range(len(row)):
                            if row[i] is not None:
                                cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
            for row in table:
                # print([re.sub('\s+', '', cell) if cell is not None else None for cell in row])
                text.append([re.sub('\s+', '', cell) if cell is not None else None for cell in row])
            # print('---------- 分割线 ----------')
    pdf.close()
    print(text)

if __name__ == "__main__":
    path = './pdf/江夏区乌龙泉石灰岩白云岩矿区国情调查表.pdf'
    pdf_tabel_func(path)
