################## IMDb演员信息爬虫 #####################
#  功能描述
#    目标：获取上IMDb上所有中国演员的获奖情况
#    输出：保存到文件中
#    技术路线：requests-bs4
###############################################################################
#  爬取网页：
#   全部演员网：http://www.imdb.com/search/name?birth_place=China&ref_=rlm
#   单个演员(巩俐)网：http://www.imdb.com/name/nm0000084/awards?ref_=nm_awd
###############################################################################
#  候选数据网站的选择：
#    选取原则：股票信息静态存在于HTML页面中,非js代码生
#              成，没有Robots协议限制。
#    选取方法：浏览器F12，源代码查看等。
#    选取心态：不要纠结于某个网站，多找信息源尝试。
########################################################
#  程序的结构设计
#    步骤1：从全部演员网站获取演员列表
#    步骤2：根据演员列表逐个到单个演员获取个人获奖信息
#    步骤3：将结果存储到文件
########################################################
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

onclick = 'http://www.imdb.com/search/name?birth_place=China&start={0}&ref_=rlm'


def getHTMLText(url, code='utf-8'):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "没有返回信息"


def getActorList(lst):
    for i in range(53):
        actorURL = onclick.format(i*50+1)
        html = getHTMLText(actorURL)
        soup = BeautifulSoup(html, 'html.parser')
        actorList = soup.find_all('div', attrs={'class': 'lister-item-image'})
        for j in actorList:
            try:
                a = j.find('a')
                href = a.attrs['href']
                lst.append(re.findall(r"[n][m]\d{7}", href)[0])
            except:
                continue
    return lst


def getAwardInfo(lst, fpath):
    count = 0
    for actor in lst:
        url = 'http://www.imdb.com/name/'+actor+'/awards?ref_=nm_awd'
        html = getHTMLText(url)
        infoDict = {}  # 字典
        list4 = {}
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')  # 煲汤
            awardInfo = soup.find('div', attrs={'class': 'article listo'})  # 爬虫主体
            namePart = awardInfo.find('h3', attrs={'itemprop': 'name'})
            a = namePart.find('a')
            name = a.string      # 获取人名
            honor_all = awardInfo.find('div', attrs={'class': 'desc'})
            if honor_all == None:
                honor = 'None'
            else:
                honor = honor_all.string      # 获取荣誉信息
            award_table = awardInfo.find_all('table', attrs={'class': 'awards'})  # 获取每个节的奖
            h3 = awardInfo.find_all('h3')  # 电影节标签
            list3 = {}
            for i in range(len(h3)-1):    # 获取电影节信息
                film_festival = h3[i+1].string
                tr = award_table[i].find_all('tr')    # 找每一年
                if tr == "":
                    break
                list2 = {}
                for j in tr:
                    try:
                        list1 = {}
                        year = j.find('td', attrs={'class': 'award_year'})
                        award_year = year.find('a').string.split()[0]  # 获奖年份
                        outcome = j.find('td', attrs={'class': 'award_outcome'})
                        award_outcome = outcome.find('b').string            # 获奖状况
                        award_category = outcome.find('span').string       # 获奖类型
                        list1[award_outcome] = award_category
                        list2[award_year] = list1
                        description = j.find('td', attrs={'class': 'award_description'})
                        if description.string == "":
                            continue
                        else:
                            descri = description.stripped_strings              # 获奖描述
                            descri = '|'.join(map(str, descri))                # 对stripped_strings类型的处理
                            descri = descri.replace(',', ' ').split('|')[0]
                            location = description.find('a').string            # 获奖地点
                            title_year = description.find('span').string       # 主题
                            list1[descri] = location + title_year
                            list2[award_year] = list1
                    except:
                        continue

                list3[film_festival] = list2
            list4[honor] = list3
            infoDict[name] = list4
##############################下面为以字典方式存储的代码##############################
#            with open(fpath, 'a', encoding='utf-8')as f:
#                f.write(str(infoDict)+'\n'+'\n')
#               # count = count + 1
#               # print('\r当前速度:{:.2f}%'.format(count * 100 / len(lst)), end='')
#######################以另一种方式存储###############################################
            with open(fpath, 'a', encoding='utf-8')as f:
                for key in infoDict:
                    f.write(str(key) + '\n')  # name
                    f.write(str(actor) + '\n')  # 编号
                    b = infoDict[key]
                    if b == "":
                        f.write('\n')
                        break
                    for key1 in b:
                        f.write(str(key1) + '\n')  # honor_all
                        c = b[key1]
                        for key2 in c:
                            f.write(str(key2) + '\n')  # festival_film
                            d = c[key2]
                            for key3 in d:
                                f.write(str(key3) + '\n')  # year_award
                                e = d[key3]
                                for key4 in e:
                                    f.write(str(key4) + '\n')  # won or nominated
                                    f.write(str(e[key4] + '\n'))  # award_type
                    f.write('\n')
                count = count + 1
                print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
        except:
            continue
    f.close()
    return infoDict


def main():
    # output_file = 'D://dictionary.txt'
    output_file1 = 'D://tree_Fixed.xls'
    alist = []
    getActorList(alist)
    print(alist)
    infoDict = getAwardInfo(alist, output_file1)
    print(len(infoDict))


main()