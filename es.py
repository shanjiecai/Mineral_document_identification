# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re
from datetime import datetime
from pprint import pprint
es_hosts = ["127.0.0.1:9200"]
es = Elasticsearch("localhost:9200")





def get_body(dataset):
    body = []
    for i in range(len(dataset)):
        print(dataset[i])
        body.append({
            "_index": "mineral_file",
            # "_id": i + 1,  # 1表示现有的es数据+1,要不会覆盖之前的数据
            "_source": {
                "filename": dataset[i]['filename'],
                "full_content": dataset[i]['full_content'],
                "entity": dataset[i]['entity'],
                "keyword": dataset[i]['keyword'],
            }
        })
    return body


def upload_data(dataset):
    print(len(dataset))
    body = get_body(dataset)
    print(body)
    helpers.bulk(es, body, index="mineral_file")  # 上传

    #  验证
    search_result = []
    # res = es.search(index='mineral_file', size=10, body={"query": {"match": {"text": "china"}}})  # 默认按照相关度排序
    # pprint(res)
    # for hit in res['hits']['hits']:
    #     # 获取指定的内容
    #     response = hit["_source"]
    #     list1 = list(response.values())
    #     print(list1)


if __name__ == '__main__':
    dataset = [{'filename': 'GQTCBG_420122402_乌龙泉矿生产矿山矿产资源国情调查报告.docx', 'full_content': '\n\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿\n生产矿山矿产资源国情调查报告\n（矿区编号：420122402）\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n武汉市自然资源和规划局\n中国冶金地质总局中南地质调查院\n二○二一年八月\n\n\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿\n生产矿山矿产资源国情调查报告\n（矿区编号：420122402）\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n目   录\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n一、矿山概况\n1 矿山基本情况\n矿山名称:武钢资源集团乌龙泉矿业有限公司乌龙泉矿\n矿山编号: 4201150084\n所属矿区：江夏区乌龙泉石灰岩白云岩矿区\n所属矿区编号：420122402\n采矿许可证编号: C4200002013026120128751\n采矿权有效期：2023.04.09\n采矿权拐点坐标等信息见采矿许可证复印件。\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿交通位置见图1，本次调查矿山与矿区归属关系与储量库一致。\n\n2 矿体地质特征\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿出露于京广线以西、鸽子山以东近东西向低山丘陵地带，东西长3.2km，南北宽0.3km～0.9km。矿层由Ⅰ号矿层（白云岩矿层）、Ⅱ号矿层（浅色石灰岩矿层），Ⅲ号矿层（深色石灰岩矿层）组成。矿层总厚度平均为184.95m，呈单斜层状产出，总体走向：15勘探线以东60°～80°，以西30°～60°，倾向南东，倾角9°～24°，局部矿块倾向南西。矿床（层）上部为石灰岩矿层，下部为白云岩矿层，之间夹石灰岩与白云岩互层。\n3.以往地质勘查工作概况\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿普查找矿工作始于1953年3月，矿山1958年与武钢同步建成投产，是国有大型矿山企业，是中国宝武武汉总部唯一的冶金熔剂原料生产基地，建矿以来生产至今。\n建矿以来陆续进行了多次地质勘查工作，详见矿区国情调查报告。矿山最新储量核实报告为《湖北省武汉市江夏区乌龙泉矿区石灰岩、白云岩矿资源储量核实报告（截至2018年4月底)》，于2019年4月以鄂自然资储备字〔2019〕26号文备案，核实报告中资源储量见表2。\n\n\n\n\n\n\n\n表2  武钢资源集团乌龙泉矿业有限公司乌龙泉矿资源储量一览表\n矿山主要矿种为熔剂用石灰岩，共生矿种为冶金用白云岩。截至2018年4月的储量核实报告2019年才评审通过，2018年底的保有资源量采用了储量核实报告中的数据。2019年年报上报了2019年全年的消耗量，当时的保有量为2018年4月数据扣除2019年全年消耗量。实际2018年5-12月的消耗量一直未统计进去。后在矿山储量数据新老标准转换时进行了扣减，转换成果通过了专家的核实和评审通过。\n表3  2018年以来乌龙泉矿资源储量变化表\n单位：千吨\n注：2019年数据采用了年报数据。\n\n4.开发利用情况\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿开采矿种为石灰岩和白云岩，矿山露天开采，采用组合台阶采矿法，生产规模270万吨/年，大型规模。1958年到2020年，乌龙泉矿经历了62年的开采，累计消耗石灰岩资源量89784千吨（探明53718千吨、控制36061千吨、推断5千吨）/储量81322千吨（证实48658千吨、可信32664千吨）；累计消耗石云岩资源量36963千吨（探明19677千吨、控制17237千吨、推断49千吨）/储量33436千吨（证实17823千吨、可信15613千吨）。2002-2020年平均回采率90.58%。目前矿山生产运行正常。\n二、本次调查工作\n本次调查工作，首先收集了省牵头单位提供的2019年矿产资源利用现状调查资料，然后从省地质资料收集到矿区最新地质报告、储量核实报告等，同时收集了武汉市江夏区矿产资源管理总站乌龙泉矿2019年储量矿山储量数据新老转换的成果、乌龙泉矿2020年储量年报，再就是积极和矿山联系，收集到了矿山最新的采矿证，最新的开发利用方案、占用矿产资源储量登记书、企业信息公示（2019、2020），些外还有测量控制点成果表、矿山成品矿生产报表2020、成品矿生产报表2021、生产报表2020、生产报表2021等资料。\n收集到的主要地质资料见表4。\n表4  地质资料目录表\n2.1 外业实测\n本次调查工作的外业测量工作之前，矿山《2020年度资源储量变化表》已通过了专家审查。重点收集了《2020年度资源储量变化表》的有关资料和现有的生产勘探资料及生产开采现状资料。对照生产矿山调查报告中矿山调查表进行了现场核验，采用全站仪、手持GPS对矿山重要探矿工程（水文孔、照片2-1）、露天采场边界、采矿权界线（照片2-2）、矿区测量控制点（照片2-3）等地进行了实测，并对动用矿体的矿石质量进行了核实检查； 系统的了解近年来的开采。根据收集的资料，室内编制了相关图件，估算了资源储量，检测保有资源储量。\n表5 乌龙泉矿2020年度动用资源储量汇总表\n2.2 图件编制\n依据内业整理和外业调查，编制完成了《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿采掘平面图》，反应了矿山矿产资源利用现状。\n编制了主矿体的新分类的矿产资源储量估算图，其他矿体的资源储量估算图采用储量年报图件。在图面上反应了矿体的采动位置、新分类的资源储量信息。\n所有图件坐标系经过了统一转换，采用2000国家大地坐标系和1985国家高程基准。所有图件图层编码及结构均按照矿产资源国情调查数据库建库要求编制。\n\n2.3 矿山数据调查表编制\n以2018年矿山储量核实报告为基础，结合2018年以来历年的矿山储量年报、2019年开发利用方案以及矿山日常生产相关技术资料，对矿山调查表进行了核实，数据信息经比对后无较大出入，仅仅是对矿山生产中“三率”及采选冶经济效益的一些动态更新。与储量库不一致的信息列入存疑问题一览表（表6）。\n表6  调查对象存疑问题一览表\n在本次调查的基础上编制了生产矿山矿产资源国情调查表和矿山矿体资源储量调查表，完善了矿山基本情况、矿山外部条件、矿床特征及主要矿体特征等基本信息，采集了新分类资源储量信息。\n2.4 质量评述\n乌龙泉矿地质首席严钦高，生产服务分公司周桐、田凯、刘文、马良元等参与了本次外业调查。\n调查数据严格依据《矿产资源国情调查技术要求（非油气部分）》及《湖北省矿产资源国情调查工作手册》，其质量满足本次调查需求，企业对调查报告内容核对后予以签字确认。企业对存疑数据进行了补充，举证材料（核实报告和动态检测报告资料、现有的生产勘探、生产开采现状资料）合法有效，满足本次矿山调查需求。\n三、调查结果\n3.1 保有资源储量\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿为生产矿山，不存在已批复压覆情况。截至2020年12 月31日，该采矿许可证范围内本次调查和储量库（2020）中保有的查明矿产资源储量对比于表7中。\n表7  乌龙泉矿2020年保有矿产资源储量对比表\n注：单位千吨。\n3.2 保有资源储量变化情况及原因\n截至2018年4月的储量核实报告直致2019年才评审通过，2018年底的保有资源量采用了储量核实报告中的数据。2019年年报上报了2019年全年的消耗量，当时的保有量为2018年4月数据扣除2019年全年消耗量。实际2018年5-12月的消耗量一直未统计进去。后在矿山储量数据新老标准转换时通过了专家的核实和评审通过。\n3.3 数据调整意见及举证说明\n（1）矿山储量数据转换结果调整说明（截至2019年）\n调整说明中指出：数据转换调整是根据“湖北省武汉市江夏区乌龙泉矿区石灰岩白云岩矿资源储量核实报告（截至2018年4月底）”(鄂自然资储备字〔2019〕26号)的保有储量，扣减2018年5-12月及2019年全年的开采消耗量后得出的。因下发的转换数据没有扣减2018年5-12月的开采消耗量（数据在我矿上报的“2019年度固体矿产资源统计基础表”中有体现），所以在调整衔接表中，对保有量进行了调减，但累计查明量没有变化。\n下发的转换保有数据（2019年储量库）为：石灰岩331:14348千吨，332:16375千吨，333:2992千吨；白云岩331:1169千吨，332:7679千吨，333:0千吨。\n调整后的保有数据为：石灰岩TM:13477千吨，KZ:16015千吨，TD:2992千吨；白云岩TM:618千吨，KZ:7374千吨，TD:0千吨。调整变化量为：石灰岩保有TM:-871千吨，KZ:-360千吨；白云岩保有TM:-551千吨，KZ:-305千吨。\n该成果通过了武汉市组织召开的专家评审会评审通过。\n（2）武汉市江夏区乌龙泉矿区石灰岩白云岩矿2020年度资源储量变化表\n该变化表在2019年矿山储量数据新老标准转换成果的基础上扣减了2020年的消耗量，结果通过了武汉市组织的专家评审会评审通过。\n变化表中的主要结论：保有石灰岩资源量30814千吨（探明12811千吨、控制15011千吨、推断2992千吨）/储量25201千吨（证实11604千吨、可信13597千吨），保有白云岩资源量6698千吨（探明618千吨、控制6080千吨）/储量6067千吨（证实560千吨、可信5507千吨）。\n四、存在的问题\n1、武钢资源集团乌龙泉矿业有限公司乌龙泉矿采矿权坐标点共计77个，其中54号拐点和71号拐点坐标完全一致，导致图形范围自相交。未必免图形相交错误，本次调查录入数据时将54号拐点往东移了1米，坐标由原来的X:3350075.99,Y:38528273.97改为X:3350075.99,Y:38528274.97。该项改动不影响矿区资源储量。\n2、矿山地质情况较复杂，以往勘查工作根据矿层的地质特征分成了三个矿体，Ⅱ号矿体又根据矿石品级，分成了Ⅱ-1、Ⅱ-2、Ⅱ-1-L、Ⅱ-2-L、Ⅱ-4等5个矿体。以往储量报告均按证内外，水平标高等来进行资源储量梳计，未按矿体进行统计。本次暂未将其分开统计填报。\n', 'keyword': 'c4200002013026120128751,湖北省武汉市江夏区,矿产资源储量,武汉市江夏区,采矿许可证,白云岩矿,生产矿山,矿山储量,乌龙泉矿,资源集团,石灰岩,白云岩', 'entity': {'pla': [], 'per': [], 'org': []}}, {'filename': 'GQTCBG_420122402_江夏区乌龙泉石灰岩白云岩矿区国情调查报告.docx', 'full_content': '\n\n湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区\n矿产资源国情调查报告\n（矿区编号：420122402）\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n武汉市自然资源和规划局\n中国冶金地质总局中南地质调查院\n二○二一年八月\n\n湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区\n矿产资源国情调查报告\n（矿区编号：420122402）\n\n\n\n\n\n\n\n\n\n目   录\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n一、矿区概况\n1.矿区基本情况\n矿区名称:江夏区乌龙泉石灰岩白云岩矿区\n矿区编号:420122402\n江夏区乌龙泉石灰岩白云岩矿区位于武汉市江夏城区178°方位，直距12km处，行政区划隶属武汉市江夏区。矿区东起京广线，西至鸽子山东坡，东西长3.4km，南北宽0.8km～1.1km，面积5.3783km2。矿区地理坐标（2000坐标系）：东经114°17′12″～114°19′05″，北纬30°15′57″～30°17′00″。矿区东侧设有专用铁路，在乌龙泉站与京广铁路相接，距武钢56km；另有公路经纸坊直通武汉市。矿区西侧有公路在段岭庙与107国道衔接，北距武昌火车站37km，南达咸宁市50km。矿区交通极为便利（见图1-1）。\n\n江夏区乌龙泉石灰岩白云岩矿1958年与武钢同步建成投产，建矿以来生产至今，矿区以往没有设立过探矿权，直接办理的采矿权。矿区经矿区梳理后，最终确定的矿区范围拐点坐标见表1-1。\n表1-1   本次调查范围拐点坐标\n2.矿业权设置情况\n矿区内有1个有效采矿权: 武钢资源集团乌龙泉矿业有限公司乌龙泉矿，没有已批复压覆情况。调查单元与该采矿权完全重合。采矿权相关信息见附件1。\n\n图1-2 江夏区乌龙泉石灰岩白云岩矿区权来权设置情况\n3.以往地质勘查工作概况\n乌龙泉矿区普查找矿工作始于1953年3月，原中华钢铁公司地质矿务处普查队根据纸坊火车站铁路工人的报矿线索对乌龙泉一带的石灰岩、白云岩矿进行了概略调查，同年8月提交了《湖北武昌乌龙泉石灰岩、白云岩矿地质勘探工作报告》。认为乌龙泉矿区距武钢近，交通方便，石灰岩、白云岩矿石质量好，蕴藏量丰富，适于露天开采，从而肯定了该矿床有详细勘探价值。\n1954年后，矿区的勘探工作由东向西分段进行，从22号勘探线向东至1号勘探线为东区，从22号勘探线向西至44号勘探线为西区，西区又称鸽子山矿段。东区在开采过程中又划分为3个采区：E100-7勘探线为1-2采区，7-15为3-4采区，15-22勘探线为5-6采区。开采标高都在43m以上。\n（1）东区勘查工作\n1954年至1955年，原重工业部地质局武汉地质勘探公司902队在1～20线进行了勘探，按100m～200米线距进行工程控制，探明石灰岩矿A2+B+C1级储量5372.8万吨，白云岩矿储量3185万吨。1956年初提交了《湖北省武昌县乌龙泉石灰石白云石矿地质勘探报告》，报告由全国储委审查，下发“全国储委复审报告决议书第301号”文批准。\n1957年至1965年，武钢乌龙泉矿在东区进行了补充勘探和生产勘探。1963年提交了《湖北省武昌县武汉钢铁公司乌龙泉石灰石白云石矿地质储量总算报告》；1965年6月提交了《湖北省武昌县武钢乌龙泉石灰石白云石矿地质储量总算报告》，后者作为前者的补充。探明石灰岩A2+B+C1级储量5649.80万吨，C2级2777.10万吨，白云岩C1级储量2272.03万吨，C2级储量5240.30万吨.该报告经湖北省储委审查，核发第53号审批决议书，以“（65）鄂储办字第18号”文批准。\n1977-1978年，湖北省冶金地质勘探公司607队在5-6采区对优质石灰岩进行了勘探。1978年6月提交了《湖北省武昌县乌龙泉石灰石矿区五、六采区优质石灰石储量计算报告书》。探明优质石灰岩矿A+B+C+D级储量5194.4万吨。报告经冶金部储委审查，“湖北省冶金工业局鄂革冶矿字（1978）539号”文批准。\n1965年-1986年，武钢在生产过程中，在1-2和3-4采区用钻探工程进行了生产勘探，及时指导了矿山开采工作 ，提高了1-4采区的勘探程度和研究程度，但对优质石灰岩没有进行专门的勘探和研究，尚缺系统资料和矿石储量。\n（2）西区勘查工作\n1972年5月至1973年11月，中南冶金地质勘探公司605队在西区进行了石灰岩、白云岩勘探，在构造简单地段勘探网度为200m×100m～200m，在构造复杂地段为50m×50m～100m。1974年元月提交《湖北省武昌县乌龙泉石灰石白云石矿区鸽子山矿段地质勘探报告书》，探明石灰岩矿B+C+D级储量8113.3万吨，白云岩矿C+D级储量4335.8万吨。1974年12月18日湖北省储委所发“报告”审批决议书认为：基本查明了西区各种矿石的厚度和质量，经不同程度的工程控制了较大断层的产状及延伸情况，取得了有害夹层、夹石、岩溶和裂隙率及其充填率的充分资料，批准地质勘探报告书可作为乌龙泉矿区鸽子山矿段设计建厂的地质依据。但对部分矿层、断层控制不够，地表裂隙观察不够，对岩溶裂隙充填物的观察研究不够。1974年12月29日武钢以（74）矿函字第027号文提出互层矿石工业指标，要求计算互层矿储量。湖北省储委以（75）鄂储办第19号文（“报告”补充审批书）批准互层矿B级储量227.9万吨，C级储量949.20万吨，D级储量243.2万吨，共1420.3万吨，作为炼铁时制造高镁炉渣配料之用。\n为满足武钢生产对活性灰用优质石灰岩的需要，中南冶勘607队于1982年5月至12月重点对优质石灰岩进行了勘探。矿区外围进行了地质草测（1:10000），修测了西区的地质图（1:1000），并对浅色石灰岩重新采样试验，地表按50m间距进行了槽探控制，深部按50m～100m×50m～100m的网度进行了钻探控制。1983年6月提交了《湖北省乌龙泉矿区鸽子山矿段优质石灰石矿勘探报告》，探明优质石灰岩矿B+C+D级储量4592.2万吨，并重新圈定和计算溶剂石灰岩矿B+C+D级储量2967.7万吨。1986年湖北省储委对报告进行了审查，因存在问题未获批准。\n报告查明或基本查明了西区的地层、构造，深色石灰岩和浅色石灰岩矿层的产状、规模及空间位置，确定了矿石类型、品级、物质组分及其变化，研究确定了夹石层的岩性、规模及其分布，并作了大致圈定，评价了矿床开采技术条件。\n2003年7月至2003年12月，中国冶勘总局中南地质勘查院对武钢乌龙泉矿西区进行了生产地质勘探工作。2004年1月提交了《武钢矿业有限责任公司乌龙泉矿西区生产地质勘探报告》，按原工业指标要求，重新估算了西区资源储量，探明西区矿石资源储量111b+122b（B+C+D级）：优质石灰岩2924.31万吨、石灰岩1973.97万吨、白云岩3181.69万吨。提交+43m以上资源储量111b+122b（B+C+D级）：优质石灰岩1975.09万吨、石灰岩1484.46万吨、白云岩1195.09万吨。\n（3）全局勘查\n武钢乌龙泉矿为了总结历年来矿山的勘探工作成果，满足矿山生产发展需要，同时提高矿山的勘探程度和研究程度，湖北省鄂东北地质大队于1986年11月至1989年11月，重新测制了矿区地质图（1:1000），勘探线剖面图，修测矿区外围水文地质图（1:10000）和矿区水文地质图（1:1000）。并对全矿区的岩溶率、裂隙率、含泥率也作了重新调查和研究，对以往三十多年来所提交的5份地质报告及矿山生产中所积累的资料进行了系统的整理和研究。提交了《湖北省武昌县乌龙泉石灰岩白云岩矿区勘探地质总结报告》，按新的工业指标要求，重算了全区资源储量，提交矿石总储量（B+C+D级）：26324.04万吨，其中优质石灰岩10551.46万吨，石灰岩5550.95万吨，白云岩10221.63万吨。提交+43m以上保有储量（B+C+D级）：13405.50万吨。其中优质石灰岩6046.37万吨，石灰岩3183.72万吨，白云岩4175.41万吨，湖北省储委以鄂储决字[1990]05号文批准其储量。\n2008年7月至2009年9月，中国冶金地质总局中南局对武钢乌龙泉矿区进行了生产地质勘探，提交了《武钢矿业有限责任公司乌龙泉石灰岩、白云岩矿地质勘探报告》，按原工业指标要求，重新估算了矿区保有资源/储量，本次探明矿区矿石保有资源/储量111b+122b（B+C+D级）：优质石灰岩5869.84万吨、石灰岩3343.69万吨、白云岩8059.16万吨。其中提交+43米以上保有资源/储量111b+122b（B+C+D级）：优质石灰岩3122.18万吨、石灰岩2142.53万吨、白云岩3159.04万吨；提交+43米以下保有资源/储量111b+122b（B+C+D级）：优质石灰岩2747.66万吨、石灰岩1201.59万吨、白云岩4900.12万吨。\n（4）储量核实情况\n2004年受武钢矿业有限责任公司乌龙泉矿的委托，中国冶勘总局中南地质勘查院对武汉市江夏区乌龙泉石灰岩白云岩矿区进行了资源储量检测工作，并于2004年12月提交了《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区2004年度矿产资源储量检测地质报告》，查明矿区矿石总量为267323.04千吨，其中探明的经济资源储量111b：75716.62千吨；控制的经济资源储量122b：191606.42千吨，保有量 192300.51千吨，报告获湖北省国土资源厅备案，批准文件：鄂土资储核函 [2005]114号。\n2007年受乌龙泉矿的委托，武钢集团矿业有限责任公司对所属乌龙泉石灰岩白云岩矿区进行了2007年度资源储量地质测量工作，并于2008年6月提交了《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区2007年度矿产资源储量检测地质报告》，查明矿区石灰岩矿资源储量为58313千吨，其中探明的经济资源储量111b：14562千吨，控制的经济资源储量122b：43751千吨；保有石灰岩资源储量 33970千吨，其中探明的经济资源储量111b：5913千吨，控制的经济资源储量122b：28057千吨；查明矿区白云岩矿资源储量为103783千吨，其中探明的经济资源储量111b：14530千吨，控制的经济资源储量122b：89253千吨；保有白云岩矿资源储量 84508千吨，其中探明的经济资源储量111b：5370千吨，控制的经济资源储量122b：79138千吨。湖北省国土资源厅以鄂土资储核函 [2008]86号文批准其储量。\n2013年受武钢集团矿业有限责任公司委托，中国冶金地质总局中南地质勘查院对本矿区进行了矿产矿产资源储量核实工作，于2013年度1月提交了《湖北省武汉市乌龙泉石灰岩白云岩矿资源储量核实报告》。截至2012年9月30日，武汉钢铁集团矿业有限责任公司采矿许可证范围内累计查明主矿产石灰岩矿资源储量11956.38万吨，其中：（111b）矿石量6846.95万吨，（122b）矿石量4897.40万吨，（333）矿石量212.03万吨；共生矿产白云岩矿资源储量5224.37万吨，其中：（111b）矿石量2140.90万吨，（122b）矿石量2992.73万吨，（333）矿石量90.74万吨。累计消耗主矿产石灰岩矿资源量7590.30万吨，其中：（111b）矿石量4376.22万吨，（122b）矿石量3214.08万吨；共生矿产白云岩矿消耗资源量2507.76万吨，其中：（111b）矿石量1262.84万吨，（122b）矿石量1240.01万吨，（333）矿石量4.91万吨。保有石灰岩矿资源储量4366.08万吨，其中：（111b）矿石量2470.73万吨，（122b）矿石量1683.32万吨，（333）矿石量212.03万吨 ；共生矿产白云岩矿资源储量2716.61万吨，其中：（111b）矿石量878.06万吨，（122b）矿石量1752.72万吨，（333）矿石量85.83万吨。报告获国土资源部备案，证明文件号为国土资储备字[2013]42号。\n2018年受武钢集团矿业有限责任公司委托，中国冶金地质总局中南地质勘查院再次对本矿区进行了矿产矿产资源储量核实工作，于2018年度11月提交了《湖北省武汉市江夏区乌龙泉矿区石灰岩、白云岩矿资源储量核实报告（截至2018年4月底)》。截至2018年4月30日，武钢矿业集团乌龙泉矿业有限公司采矿许可证范围内累计查明主矿产石灰岩矿资源储量120598千吨，其中：（111b）矿石量66529千吨，（122b）矿石量51072千吨，（333）矿石量2997千吨；共生矿产白云岩矿资源储量43661千吨，其中：（111b）矿石量20295千吨，（122b）矿石量23317千吨，（333）矿石量49千吨。累计消耗主矿产石灰岩矿资源量85205千吨，其中：（111b）矿石量51020千吨，（122b）矿石量34180千吨，（333）矿石量5千吨；共生矿产白云岩矿消耗资源量33479千吨，其中：（111b）矿石量18232千吨，（122b）矿石量15198千吨，（333）矿石量49千吨。保有石灰岩矿资源储量35393千吨，其中：（111b）矿石量15509千吨，（122b）矿石量16892千吨，（333）矿石量2992千吨 ；共生矿产白云岩矿资源储量10181千吨，其中：（111b）矿石量2063千吨，（122b）矿石量8119千吨，（333）矿石量0千吨。43～0m标高以下（证外）计算查明矿石量88104千吨。查明石灰岩矿资源储量40021千吨，其中：（111b）矿石量8376千吨，（122b）矿石量11289千吨，（333）矿石量20356吨；查明白云岩矿资源储量48083千吨，其中（111b）矿石量7357千吨，（122b）矿石量17102吨，（333）矿石量23624千吨。报告获湖北省国土资源厅备案，证明文件号为鄂自然资储备字〔2019〕26号。\n4.开发利用情况\n武钢资源集团乌龙泉矿业有限公司乌龙泉矿开采矿种为石灰岩和白云岩，矿山露天开采，采用组合台阶采矿法，生产规模270万吨/年，大型规模。1958年到2020年，乌龙泉矿经历了62年的开采，累计消耗石灰岩资源量89784千吨（探明53718千吨、控制36061千吨、推断5千吨）/储量81322千吨（证实48658千吨、可信32664千吨）；累计消耗石云岩资源量36963千吨（探明19677千吨、控制17237千吨、推断49千吨）/储量33436千吨（证实17823千吨、可信15613千吨）。2002-2020年平均回采率90.58%。目前矿山生产运行正常。\n二、本次调查工作\n1.内业整理\n（1）资料收集\n本次调查工作，首先收集了省牵头单位提供的2019年矿产资源利用现状调查资料，然后从省地质资料收集到矿区最新地质报告、储量核实报告等，同时收集了武汉市江夏区矿产资源管理总站乌龙泉矿2019年储量矿山储量数据新老转换的成果、乌龙泉矿2020年储量年报，再就是积极和矿山联系，收集到了矿山最新的采矿证，最新的开发利用方案、占用矿产资源储量登记书、企业信息公示（2019、2020），些外还有测量控制点成果表、矿山成品矿生产报表2020、成品矿生产报表2021、生产报表2020、生产报表2021等资料。\n收集到的主要地质资料见表2-1。\n表2-1  地质资料目录表\n（2）矿区梳理\n江夏区乌龙泉石灰岩白云岩矿1958年与武钢同步建成投产，建矿以来生产至今，矿区以往没有设立过探矿权，直接办理的采矿权。\n通过对以往资料的进一步核实，以往工作均以武钢资源集团乌龙泉矿业有限公司乌龙泉矿采矿证范围为工作区，工作区拐点较多且复杂。为方便工作，通过梳理，最终确定了本次矿区范围（见表1-1）。\n通过对武钢资源集团乌龙泉矿业有限公司乌龙泉矿进行梳理，发现下发数据中矿山名称中存在错别字，已改正。没有已批得的压覆情况存在。见表2-2。\n表2-2  梳量前后调查单元及其具体调查对象一览表\n（3）数据整理情况\n①根据储量库形成本底数据\n本次调查本底数据由省牵头单位整理下发，另已形成矿区矿产资源国情调查表。\n②信息补充\n矿区调查表信息缺项较多，依据收集到的地质资料对该表进行了补充。同时导出矿区内采矿权的矿山调查表，对调查表缺失的内容进行了初步补充。并填写了内业整理存疑问题梳理情况一览表（表2-3）。\n表2-3  内业整理存疑问题梳理情况一览表\n\n③矿体调查表编制\n依据本次收集到的矿山地质资料，填写“矿体资源储量调查表”，由于矿区矿体复杂，未分矿体统计资源储量。\n经检查发现，乌龙泉矿一直正常生产，每年矿山都有消耗量，企业在矿产2020年储量年报中矿体资源储量估算图与矿体调查表数据能扣合。\n④图件整理\n通过收集到的资料经过矿区梳理，依据矿区空间信息形成了《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区平面套合图》，理清了调查单元和调查对象的空间关系。\n将收集到的矿山2018年储量核实报告中所有矿体储量估算图，结合近几年矿山储量年报中的动用情况，修编完成乌龙泉矿体资源储量估算图底图，作为外业调查依据。\n（4）存在问题梳理\n①与矿山生产有关的一些信息，需要到矿山实际进行收集。\n②生产矿山资料的真实性，需要通过外业调查验证。\n2.外业调查\n（1）乌龙泉矿外业调查\n调查队伍对生产矿山调查过程及成果进行了检查核实。\n①对生产矿山调查报告中矿山调查表进行了现场核验，没有发现明显问题。\n②采用全站仪、手持GPS对矿山重要探矿工程（水文孔、照片2-1）、露天采场边界、采矿权界线（照片2-2）、矿区测量控制点（照片2-3）等地进行了实测，并对动用矿体的矿石质量进行了核实检查，实测结果与生产矿山调查报告基本吻合。（见表2-3、表2-4、表2-5）。对部分不具务实测条件的地方，企业技术人员提供了举证材料，调查全过程留存了影像记录，外业调查完成后矿山企业对调查结果认可并在矿山调查表上签字确认。\n\n照片2-1  乌龙泉水文孔实测\n\n照片2-2  乌龙泉采矿权边界实测\n\n照片2-3  乌龙泉测量控制点实测\n表2-3  乌龙泉矿水文孔孔口坐标实测检验表\n\n表2-4  乌龙泉矿采矿权边界实测对照表\n\n表2-4  乌龙泉矿测量控制点实测对照表\n\n\n（2）存疑数据解决情况\n①通过外业调查和矿山相关部门的沟通，补充收集了矿山生产和经济数据。\n②通过外业实地测量和调查，验证了生产矿山资料均与年报等提供的数据一致。\n3.图件编制\n依据内业整理和外业调查，编制完成了《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿区平面套合图》、《湖北省武汉市江夏区乌龙泉石灰岩白云岩矿采掘平面图即利用现状图》。还收集了江夏区乌龙泉石灰岩白云岩矿区典型勘探线剖面图\n所有图件坐标系经过了统一转换，采用2000国家大地坐标系和1985国家高程基准。所有图件图层编码及结构均按照矿产资源国情调查数据库建库要求编制。\n4.矿区数据调查表编制\n经室内整理，结合2019年矿产资源储量新老分类标准数据转换成果和矿山2020年储量变化表数据，核实编制了《江夏区乌龙泉石灰岩白云岩矿区资源储量调查表》和《武钢资源集团乌龙泉矿业有限公司乌龙泉矿资源储量调查表》。\n经室内整理和外业调查，补充完善了“江夏区乌龙泉石灰岩白云岩矿区矿产资源国情调查表”中的缺失信息，对矿区内矿山的资源储量依据本次《矿产资源国情调查技术要求（非油气）》进行了调查统计，按照最新的矿产资源储量分类对调查结果进行了套改检查，同时修改了内业数据整理中发现的问题。矿产资源国情调查表信息变更及说明见表2-5。\n表2-5 矿产资源国情调查表信息变更及说明对照表\n\n5.质量评述\n调查过程中认真执行了《湖北省矿产资源国情调查工作手册（非油气）》和《矿产资源国情调查数据库建设技术（非油气）》及相关地质技术规范要求，严格按照我院质量管理体系开展工作，确保院～项目组～作业组三级质量保障体系正常运行。\n市级和省级质量检查尚未开展，暂未进行。\n三、调查结果\n1.保有资源储量\n通过本次调查，乌龙泉矿区（采矿证内）保有资源储量为：保有石灰岩资源量30814千吨（探明12811千吨、控制15011千吨、推断2992千吨）/储量25201千吨（证实11604千吨、可信13597千吨），保有白云岩资源量6698千吨（探明618千吨、控制6080千吨）/储量6067千吨（证实560千吨、可信5507千吨）。\n表3-1  江夏区乌龙泉石灰岩白云岩矿区本次调查与储量库保有资源储量对比表\n注：所有数据均为矿石量，单位为千吨。\n通过收集生态红线、卫星图片、高速公路、永久基本农田、自然保护区和压覆备案等数据，对比可知江夏区乌龙泉石灰岩白云岩矿区全区范围内不存在与上述重点功能区重叠情况。\n2.保有资源储量变化情况及原因\n截至2018年4月的储量核实报告直致2019年才评审通过，2018年底的保有资源量采用了储量核实报告中的数据。2019年年报上报了2019年全年的消耗量，当时的保有量为2018年4月数据扣除2019年全年消耗量。实际2018年5-12月的消耗量一直未统计进去。后在矿山储量数据新老标准转换时通过了专家的核实和评审通过。\n3.数据调整意见及举证说明\n（1）矿山储量数据转换结果调整说明（截至2019年）\n调整说明中指出：数据转换调整是根据“湖北省武汉市江夏区乌龙泉矿区石灰岩白云岩矿资源储量核实报告（截至2018年4月底）”(鄂自然资储备字〔2019〕26号)的保有储量，扣减2018年5-12月及2019年全年的开采消耗量后得出的。因下发的转换数据没有扣减2018年5-12月的开采消耗量（数据在我矿上报的“2019年度固体矿产资源统计基础表”中有体现），所以在调整衔接表中，对保有量进行了调减，但累计查明量没有变化。\n下发的转换保有数据（2019年储量库）为：石灰岩331:14348千吨，332:16375千吨，333:2992千吨；白云岩331:1169千吨，332:7679千吨，333:0千吨。\n调整后的保有数据为：石灰岩TM:13477千吨，KZ:16015千吨，TD:2992千吨；白云岩TM:618千吨，KZ:7374千吨，TD:0千吨。调整变化量为：石灰岩保有TM:-871千吨，KZ:-360千吨；白云岩保有TM:-551千吨，KZ:-305千吨。\n该成果通过了武汉市组织召开的专家评审会评审通过。\n（2）武汉市江夏区乌龙泉矿区石灰岩白云岩矿2020年度资源储量变化表\n该变化表在2019年矿山储量数据新老标准转换成果的基础上扣减了2020年的消耗量，结果通过了武汉市组织的专家评审会评审通过。\n变化表中的主要结论：保有石灰岩资源量30814千吨（探明12811千吨、控制15011千吨、推断2992千吨）/储量25201千吨（证实11604千吨、可信13597千吨），保有白云岩资源量6698千吨（探明618千吨、控制6080千吨）/储量6067千吨（证实560千吨、可信5507千吨）。\n四、存在的问题及建议\n1、矿区、矿山没有经过探矿权再升级到采矿权的过程，矿区范围为本次调查重新确定。\n2、矿山资源储量估算范围，在2013年，2018年储量核实报告中有提及，但范围比实际矿体水平投影范围要大。通过核实，本次按实际情况更新了资源储量估算范围，使之与实际储量估算工作涉及的矿体块断一致。\n3、武钢资源集团乌龙泉矿业有限公司乌龙泉矿采矿权坐标点共计77个，其中54号拐点和71号拐点坐标完全一致，导致图形范围自相交。未必免图形相交错误，本次调查录入数据时将54号拐点往东移了1米，坐标由原来的X:3350075.99,Y:38528273.97改为X:3350075.99,Y:38528274.97。该项改动不影响矿区资源储量。\n4、矿山地质情况较复杂，以往勘查工作根据矿层的地质特征分成了三个矿体，Ⅱ号矿体又根据矿石品级，分成了Ⅱ-1、Ⅱ-2、Ⅱ-1-L、Ⅱ-2-L、Ⅱ-4等5个矿体。以往储量报告均按证内外，水平标高等来进行资源储量梳计，未按矿体进行统计。本次暂未将其分开统计填报。\n', 'keyword': '湖北省武汉市江夏区,矿产资源储量,武汉市江夏区,地质勘探报告,白云岩矿,石灰岩矿,共生矿产,乌龙泉矿,资源集团,矿石量,江夏区,石灰岩,白云岩', 'entity': {'pla': [], 'per': [], 'org': []}}]
    upload_data(dataset)