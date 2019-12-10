# coding:utf-8
# 汽车之家论坛数据字体反爬

import re

import requests

from scrapy import Selector

from fontTools.ttLib import TTFont
from pprint import pprint


class QiCheZhiJiaSpider:

    def article_content(self):

        url = 'https://club.autohome.com.cn/bbs/thread/2d8a42404ba24266/77486027-1.html#pvareaid=2199101'

        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'

        }

        try:

            response = requests.get(url=url, headers=headers).text

            response_info = Selector(text=response)

        except BaseException as e:

            print(e)

        else:

            content = response_info.xpath('//div[@class="tz-paragraph"]//text()').extract()  # 获取列表的形式内容。

            content_str = ''.join(content)

            # 紧接着获取字体的链接

            word_href = re.findall(r",url\('(//.*\.ttf)'\).*", response, re.M or re.S)[0]

            word_href = 'https:' + word_href

            word_content = requests.get(url=word_href, headers=headers).content

            # 对获取到的字体进行下载..........

            with open('./word.ttf', 'wb') as f:

                f.write(word_content)

            # 那么便开始通过字体库进行解析

            word = TTFont('./word.ttf')

            # 读取响应的映射关系,获取unicode编码

            # 'cmap' 表示汉字对应的映射 为unicode编码

            uni_list = word['cmap'].tables[0].ttFont.getGlyphOrder()

            # 按顺序拿到各个字符的unicode编码

            print(uni_list)
            """
            结果为:.notdef 并不是汉字的映射， 而是表示字体家族名称
            ['.notdef', 'uniEC5F', 'uniEDA0', 'uniECED', 'uniED3E', 'uniEC8B', 'uniECDD', 'uniEC29', 'uniED6A',
             'uniEDBC', 'uniED08', 'uniEC55', 'uniECA7', 'uniEDE7', 'uniEC45', 'uniED86', 'uniECD2', 'uniED24',
             'uniEC71', 'uniEDB1', 'uniEE03', 'uniED50', 'uniEDA2', 'uniECEE', 'uniEC3B', 'uniEC8D', 'uniEDCD',
             'uniED1A', 'uniED6C', 'uniECB8', 'uniED0A', 'uniEC57', 'uniED97', 'uniEDE9', 'uniED36', 'uniEC82',
             'uniECD4', 'uniEC21', 'uniEC72']
             """

            # 将映射列表转换成unicode的类型，因为自己文中获取的是字符串unicode类
            # 型的，当然你也可以转化为utf-8,不过你获取的文章内容也要转化为utf-8

            unicode_list = [eval(r"u'\u" + uni[3:] + "'") for uni in uni_list[1:]]

            print(unicode_list)
            """
            结果为:
            ['\uec5f', '\ueda0', '\ueced', '\ued3e', '\uec8b', '\uecdd', '\uec29', '\ued6a', '\uedbc', '\ued08',
             '\uec55', '\ueca7', '\uede7', '\uec45', '\ued86', '\uecd2', '\ued24', '\uec71', '\uedb1', '\uee03',
             '\ued50', '\ueda2', '\uecee', '\uec3b', '\uec8d', '\uedcd', '\ued1a', '\ued6c', '\uecb8', '\ued0a',
             '\uec57', '\ued97', '\uede9', '\ued36', '\uec82', '\uecd4', '\uec21', '\uec72']

            """

            # 通过fontcreator软件查看获取word.ttf中的字体!该字体网站会隔一段时间变更,所以每次需要查看一下

            word_list = ["三", "四", "坏", "和", "五", "低", "远", "二", "上", "很", "高", "的", "呢", "长",

                         "多", "七", "十", "八", "矮", "下", "一", "九", "地", "少", "小", "得", "了",

                         "大", "左", "更", "好", "不", "六", "近", "是", "短", "右", "着"]

            for i in range(len(unicode_list)):

                content_str = content_str.replace(unicode_list[i], word_list[i])

            pprint(content_str)


if __name__ == '__main__':

    spider = QiCheZhiJiaSpider()

    spider.article_content()
