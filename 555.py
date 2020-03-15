#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/24 22:36
# @Author  : 亦轩
# @File    : 555.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import jieba
import jieba.analyse
# 文章关键词挖掘
def text_to_keywords(text):
    keywords = jieba.analyse.extract_tags(text,topK=5,withWeight=False)
    keywords_length = []
    for keyword in keywords:
        length = len(keyword)
        utf8_length = len(keyword.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        keywords_length.append([int(length),0])
    # keywords_str = []
    keywords_str = ''
    for list_num in range(len(keywords_length)):
        if keywords_length[list_num][1] == 0:
            keywords_length[list_num][1] = 1
            for list_num2 in range(len(keywords_length)):
                if keywords_length[list_num2][1] == 0:
                    sum_len = keywords_length[list_num2][1] + keywords_length[list_num][1]
                    if sum_len == 5:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        # keywords_str.append(str_keyword)
                        keywords_str +=str_keyword +','
                        break
                    elif sum_len < 6:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        # keywords_str.append(str_keyword)
                        keywords_str += str_keyword + ','
                        break
    return keywords_str

s = '''中新网2月24日电 据欧联通讯社报道，受新冠肺炎病毒疫情影响，意大利足球甲级联赛23日的4场赛事已被迫延期，国际米兰队原定下周的欧霸赛事也充满了变数。威尼斯狂欢节最后几天的活动也因疫情蔓延被叫停。

　　据报道，就在国际米兰对桑普多利亚、亚特兰大对萨索罗、维罗纳对卡利亚里等意大利足球甲级联赛赛事宣布推迟比赛后，都灵对帕尔马23日在都灵市的比赛也被迫宣告取消。国际米兰原定27日与保加利亚球队卢多戈雷茨进行的欧足联欧洲联赛主场赛事，如今也充满了变数。

　　意大利紧急民防部部长安吉洛•博雷利(Angelo Borrelli)23日指出，意大利全国境内已有157人新冠肺炎病毒检测出呈阳性反应，已造成3名患者不治病逝。目前当局正在采取措施强力应对疫情蔓延。

　　意大利总理孔特表示，将考虑采取非常规措施应对新冠肺炎病毒疫情，北部地区将停止一切体育赛事和集会。

　　意大利青年政策和体育部长文森佐•斯帕佛拉(Vincenzo Spadafora)表示，我们必须严肃对待新冠肺炎病毒疫情，保持冷静和有效规避风险。基于上述原因，当局决定暂停在病毒可能散播区域的所有体育赛事。

　　威尼托大区主席卢卡•扎亚(Luca Zaia)23日则表示，为进一步控制新冠肺炎病毒蔓延，预防群体交叉传播，大区政府决定取消威尼斯狂欢节最后几天的活动。他强调，威尼斯23日的活动将照原定计划进行，从23日傍晚开始至3月1日，威尼斯狂欢节所有文化活动，以及随后将举行的所有体育活动和赛事全部取消。(博源)'''

print(text_to_keywords(s))