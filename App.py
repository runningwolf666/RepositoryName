#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# Created: 2015-08-20 Thursday 
# Description: Description

请在Python3下运行此程序='Please run this program with Python3'

import time
import requests  # 快速上手： http://cn.python-requests.org/zh_CN/latest/user/quickstart.html 本页内容为如何入门Requests提供了很好的指引。
from lxml import html


def downloadPic(url, num):
    headers = {
        'Host': 'www.meizitu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-cn,en-us;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate'
    }

    try:
        page = requests.get(url, headers=headers)
    # 错误与异常
    # 遇到网络问题（如：DNS查询失败、拒绝连接等）时，Requests会抛出一个 ConnectionError 异常。
    # 遇到罕见的无效HTTP响应时，Requests则会抛出一个 HTTPError 异常。
    # 若请求超时，则抛出一个 Timeout 异常。
    # 若请求超过了设定的最大重定向次数，则会抛出一个 TooManyRedirects 异常。
    # 所有Requests显式抛出的异常都继承自 requests.exceptions.RequestException 。
    except requests.exceptions.RequestException:
        print('网络异常.')
        # sys.exit()
    else:
        page.encoding = 'gb2312'
        doc = html.document_fromstring(page.text)

        imgsrclist, imgaltlist = [], []

        # html body div#wrapper div#container div#pagecontent div#maincontent div.postContent div#picture p img
        imgs = doc.cssselect('div#maincontent div.postContent div#picture p img')
        for img in imgs:
            imgsrclist.append(img.get('src'))        
            imgaltlist.append(img.get('alt'))

        # print(imgsrclist, imgaltlist)
        for index,imgsrc in enumerate(imgsrclist):
            try:
                imgcontent = requests.get(imgsrc, headers=headers)
            except requests.exceptions.RequestException:
                print('网络异常.')
                # sys.exit()
            else:
                picname = str(num)+'_'+imgaltlist[index]+'.jpg'
                with open(picname, 'wb') as f:
                    f.write(imgcontent.content)
                print('download {}'.format(picname))


if __name__ == '__main__':
    for num in range(4033, 5011):
        url = 'http://www.meizitu.com/a/{}.html'.format(num)
        downloadPic(url, num=num)
        time.sleep(0.3)
    # url = 'http://www.meizitu.com/a/{}.html'.format(4839)
    # downloadPic(url, num=4839)
