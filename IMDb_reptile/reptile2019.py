# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

onclick = 'http://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2015-12-31&countries=us&languages=en&count=250&start={0}&ref_=adv_nxt'
pathOne ='https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2005-12-31&countries=us&languages=en&count=250&start={0}&ref_=adv_nxt'
pathTwo = 'https://www.imdb.com/search/title?title_type=feature&release_date=2006-01-01,2009-12-31&countries=us&languages=en&start={0}&ref_=adv_nxt'
pathThree = 'https://www.imdb.com/search/title?title_type=feature&release_date=2010-01-01,2012-12-31&countries=us&languages=en&count=250&start={0}&ref_=adv_nxt'
pathFour = 'https://www.imdb.com/search/title?title_type=feature&release_date=2013-01-01,2015-12-31&countries=us&languages=en&count=250&start={0}&ref_=adv_nxt'


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

    # 1-7283
    for i1 in range(30):
        print(i1)
        actorURL = pathOne.format(1+250*i1)
        html = getHTMLText(actorURL)
        soup = BeautifulSoup(html, 'html.parser')
        actorList = soup.find_all('div', attrs={'class': 'lister-item-image'})

        for j in actorList:
            try:
                a = j.find('a')
                href = a.attrs['href']

                # print(href.split("/")[2])
                lst.append(href.split("/")[2])
            except:
                continue
    print("the first part of lst's length:")
    print(len(lst))
    # 1-8233
    for i2 in range(165):
        print(i2)
        actorURL = pathTwo.format(1 + 50 * i2)
        html = getHTMLText(actorURL)
        soup = BeautifulSoup(html, 'html.parser')
        actorList = soup.find_all('div', attrs={'class': 'lister-item-image'})

        for j in actorList:
            try:
                a = j.find('a')
                href = a.attrs['href']

                # print(href.split("/")[2])
                lst.append(href.split("/")[2])
            except:
                continue
    print("the second part of lst's length:")
    print(len(lst)-7283)
    # 1-8444
    for i3 in range(34):
        print(i3)
        actorURL = pathThree.format(1 + 250 * i3)
        html = getHTMLText(actorURL)
        soup = BeautifulSoup(html, 'html.parser')
        actorList = soup.find_all('div', attrs={'class': 'lister-item-image'})

        for j in actorList:
            try:
                a = j.find('a')
                href = a.attrs['href']

                # print(href.split("/")[2])
                lst.append(href.split("/")[2])
            except:
                continue
    print("the third part of lst's length:")
    print(len(lst)-7283-8233)
    # 1-9647
    for i4 in range(39):
        print(i4)
        actorURL = pathFour.format(1 + 250 * i4)
        html = getHTMLText(actorURL)
        soup = BeautifulSoup(html, 'html.parser')
        actorList = soup.find_all('div', attrs={'class': 'lister-item-image'})

        for j in actorList:
            try:
                a = j.find('a')
                href = a.attrs['href']

                # print(href.split("/")[2])
                lst.append(href.split("/")[2])
            except:
                continue
    print("the forth part of lst's length:")
    print(len(lst)-7283-8444-8233)
    return lst


def getAwardInfo(lst, fpath):
    count = 0

    res = ['movieid', 'year', 'rate (/)', 'total votes', 'MPAA', '时长','genre','release date','reviews','metascore','budget','opening week','gross','culmulative worldwide gross','technical specs']
    f = open(fpath, 'w')
    f.writelines(','.join(res) + '\n')

    for actor in lst:
        url = 'http://www.imdb.com/title/'+actor+'/?ref_=adv_li_tt'
        html = getHTMLText(url)
        count +=1
        res[0] = actor  # 第一个参数
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')  # 煲汤

###########################################       第一块   ##############################

            filmInfo = soup.find('div', attrs={'class': 'title_bar_wrapper'})  # 爬虫主体
            # print(filmInfo)
            res[1] = filmInfo.find('span', attrs={'id': 'titleYear'}).find('a').string.replace("\n","")  # year
            res[2] = filmInfo.find('span', attrs={'itemprop': 'ratingValue'}).string.replace("\n","")      # rate
            res[3] = filmInfo.find('span', attrs={'itemprop': 'ratingCount'}).string.replace(",","").replace("\n","")       # total votes

            mpaa = filmInfo.find('div',attrs={'class':'subtext'}).stripped_strings        # MPAA
            res[4] = ''.join(map(str, mpaa)).replace(",","&").replace("\n","")

            res[5] = filmInfo.find('time').string.replace("\n","").replace(" ","")       # 时长

            genre = filmInfo.find('div',attrs={'class':'subtext'}).find_all('a',attrs={'href': re.compile('search')})   # genre
            mer_str =[]
            for j in genre:
                mer_str.append(j.string)
            # print('|'.join(map(str,mer_str)))
            res[6] = '|'.join(map(str,mer_str)).replace("\n","")
            res[7] = filmInfo.find('div', attrs={'class': 'subtext'}).find('a',attrs={'href': re.compile('releaseinfo')}).string.replace("\n","")    # release date


#############################################   第二块   #########################################

            reviInfo = soup.find('div', attrs={'class': 'titleReviewBar'})
            # print(reviInfo)
            reviews = reviInfo.find('div',attrs={'class':'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')  # reviews
            me_str=[]
            for k in reviews:
                me_str.append(k.string)
            res[8] = '|'.join(map(str, me_str)).replace(",","").replace("\n","")                        # metascore
            if reviInfo.find('div', attrs={'class': re.compile('metacriticScore')}) == None:
                res[9] = ""
            else:
                res[9] = reviInfo.find('div', attrs={'class': re.compile('metacriticScore')}).find('span').string.replace("\n","")
##############################################  第三块  ########################################

            BoxInfo = soup.find('div', attrs={'class': 'article','id':'titleDetails'})
            txtAll = BoxInfo.find_all('div',attrs={'class': 'txt-block'})
            r = {}
            for m in txtAll:
                value = m.stripped_strings
                value = ''.join(map(str, value))
                if value.find(':')==-1:
                    continue
                value = value.split(":")

                r[value[0]]=value[1]
                # print(value[0]+':::::'+r[value[0]])
            if "Budget" in r.keys():
                res[10] = r.get("Budget").replace(",","").replace("\n","").encode('utf-8')       # Budget
            else:
                res[10] = ""
            if "Opening Weekend USA" in r.keys():
                openWeek = r.get("Opening Weekend USA").replace("\n","").split(",")            # opening week
                openW = ""
                for o in openWeek:
                    if len(o) < 4:
                        openW +=o
                    else:
                        openW += '/'
                        openW += o
                res[11] = openW.encode('utf-8')
            else:
                res[11] = ""
            if "Gross USA" in r.keys():
                res[12] = r.get("Gross USA").replace(",","").replace("\n","").encode('utf-8')                  # gross
            else:
                res[12] = ""
            if "Cumulative Worldwide Gross" in r.keys():
                res[13] = r.get("Cumulative Worldwide Gross").replace(",","").replace("\n","").encode('utf-8')              # culmulative worldwide gross
            else:
                res[13] = ""
            tech = {}
            if "Runtime" in r.keys():
                tech["Runtime"] = r.get("Runtime").replace("\n","")
            if "Sound Mix" in r.keys():
                tech["Sound Mix"] = r.get("Sound Mix").replace("\n","")
            if "Color" in r.keys():
                tech["Color"] = r.get("Color").replace("\n","")
            if "Aspect Ratio" in r.keys():
                tech["Aspect Ratio"] = r.get("Aspect Ratio")+":1".replace("\n","")
            res[14] = tech                                                             # technical specs
            f.writelines(','.join(map(str, res)) + '\n')
        except:
            print(res[0]+'\n')
            continue
        print(res)
        print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
    f.close()


def main():
    # output_file = 'D://dictionary.txt'
    output_file1 = 'E://tree_Fixed.csv'
    alist = []
    getActorList(alist)
    print("length of alist:")
    print(len(alist))

    getAwardInfo(alist, output_file1)
    # print(len(infoDict))


main()
