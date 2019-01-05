# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

onclick = 'http://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2015-12-31&countries=us&languages=en&count=250&start={0}&ref_=adv_nxt'
         # https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2015-12-31&countries=us&languages=en&count=250&after=WzExNDczOCwidHQwMjAxNDg0IiwxMDAwMV0%3D&ref_=adv_nxt
        #  https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2015-12-31&countries=us&languages=en&count=250&after=WzEyMDEwNywidHQxMDk1NDA0IiwxMDI1MV0%3D&ref_=adv_nxt
def getHTMLText(url, code='utf-8'):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "没有返回信息"


def getActorList(lst,index):
    for i in range(index):
        print(i)
        actorURL = onclick.format(1+250*i)
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
            res[1] = filmInfo.find('span', attrs={'id': 'titleYear'}).find('a').string  # year
            res[2] = filmInfo.find('span', attrs={'itemprop': 'ratingValue'}).string     # rate
            res[3] = filmInfo.find('span', attrs={'itemprop': 'ratingCount'}).string.replace(",","")      # total votes

            mpaa = filmInfo.find('div',attrs={'class':'subtext'}).stripped_strings        # MPAA
            res[4] = ''.join(map(str, mpaa)).replace(",","&")

            res[5] = filmInfo.find('time').string.replace("\n","").replace(" ","")       # 时长

            genre = filmInfo.find('div',attrs={'class':'subtext'}).find_all('a',attrs={'href': re.compile('search')})   # genre
            mer_str =[]
            for j in genre:
                mer_str.append(j.string)
            # print('|'.join(map(str,mer_str)))
            res[6] = '|'.join(map(str,mer_str))
            res[7] = filmInfo.find('div', attrs={'class': 'subtext'}).find('a',attrs={'href': re.compile('releaseinfo')}).string.replace("\n","")    # release date

#############################################   第二块   #########################################

            reviInfo = soup.find('div', attrs={'class': 'titleReviewBar'})
            # print(reviInfo)
            reviews = reviInfo.find('div',attrs={'class':'titleReviewBarItem titleReviewbarItemBorder'}).find_all('a')  # reviews
            me_str=[]
            for k in reviews:
                me_str.append(k.string)
            res[8] = '|'.join(map(str, me_str)).replace(",","")
            res[9] = reviInfo.find('div', attrs={'class': 'metacriticScore score_mixed titleReviewBarSubItem'}).find('span').string                          # metascore

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

            res[10] = r.get("Budget").replace(",","")     # Budget
            openWeek = r.get("Opening Weekend USA").split(",")            # opening week
            openW = ""
            for o in openWeek:
                if len(o) < 4:
                    openW +=o
                else:
                    openW += '/'
                    openW += o
            res[11] = openW
            res[12] = r.get("Gross USA").replace(",","")                  # gross
            res[13] = r.get("Cumulative Worldwide Gross").replace(",","")              # culmulative worldwide gross

            tech = {}
            tech["Runtime"] = r.get("Runtime")
            tech["Sound Mix"] = r.get("Sound Mix")
            tech["Color"] = r.get("Color")
            tech["Aspect Ratio"] = r.get("Aspect Ratio")+":1"
            res[14] = tech                                                             # technical specs

        except:
            continue
        print(res)
        f.writelines(','.join(map(str, res)) + '\n')
        print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
    f.close()


def main():
    # output_file = 'D://dictionary.txt'
    output_file1 = 'E://tree_Fixed.csv'
    alist = []
    getActorList(alist,40)      #  能抓到10000条数据
    print(alist)

    getAwardInfo(alist, output_file1)
    # print(len(infoDict))


main()