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

            # 读取响应的映射关系,获取unicode映射值

            uni_list = word['cmap'].tables[0].ttFont.getGlyphOrder()

            print(uni_list)

            # 将映射值重新构造!这样就可以与响应中的编码相匹配

            unicode_list = [eval(r"u'\u" + uni[3:] + "'") for uni in uni_list[1:]]

            print(unicode_list)

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
