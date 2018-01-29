# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import time


##########################爬取豆瓣电影网的电影信息#########################
#     1.电影数量为6698部，用getMovieUrl函数来得到所有电影的id，从而确定url
#     2.爬取单个电影的网页用getMovieInfo函数完成
#     3.将信息存入文档
########################################################################

onclick = 'https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%A4%A7%E9%99%86&start={0}'
urlclick = 'https://movie.douban.com/subject/{}/'

cookies = {'Cookie':'ll="108288"; bid=QPeyJBpC844; ps=y; gr_user_id=b9272825-9a9d-408f-9dba-7c89201f297b; viewed="26986954_27113800"; frodotk="d3f35de49fb7073e7bda19addf2515ba"; __utma=30149280.1796725684.1516029981.1516671696.1516685733.12; __utmb=30149280.2.10.1516685733; __utmc=30149280; __utmz=30149280.1516685733.12.2.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; __utmv=30149280.17294; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=E11A9229BB62B9B4E38D2928E3025A98|92cdb5c62c8bed591ca0ab9bd495257a; ap=1; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F27133038%2F"; ck=nXg5; dbcl2="172948998:ZF1IvcjW7UE"'}


def getHTMLText(url, code='utf-8'):
    try:
        time.sleep(random.randint(1, 3))
        kv = {'user-agent': 'Mozilla/5.0'}
        proxies = {'http': 'http://117.36.103.170:8118'}
        r = requests.get(url, headers=kv, timeout=30, proxies=proxies, cookies=cookies)
        r.raise_for_status()
        print(r.status_code)
        r.encoding = code
        return r.text
    except:
        return "没有返回信息"


def getMovieUrl(urllist):
    try:
        for i in range(335):
            url = onclick.format(i*20)
            dic = getHTMLText(url)
            dic = eval(dic)   # 将字符串类型转换为字典类型
            lis = []
            for key in dic:
                lis = dic[key]
            for j in range(len(lis)):
                for key_ in lis[j]:
                    if key_ == 'id':
                        urllist.append(lis[j][key_])
        return urllist
    except:
        return"访问失败"


def getMovieInfo(movieurl, fpath, rect):
    f = open(fpath, 'w')
    f.writelines(','.join(rect)+'\n')
    for movie in movieurl:
        try:
            movieInfo = []
            url = urlclick.format(movie)
            r = getHTMLText(url)
            soup = BeautifulSoup(r, 'html.parser')
            Infoareaone = soup.find('div', attrs={'id': 'content'})
            Infoareatwo = soup.find('div', attrs={'class': 'subject-others-interests-ft'})  # 包含想看的人的信息

            Infoareaoneone = Infoareaone.find('div', attrs={'id': 'info'})            # 将区域一再分为两部分
            Infoareaonetwo = Infoareaone.find('div', attrs={'id': 'interest_sectl'})

            moviename = Infoareaone.find('span', attrs={'property': 'v:itemreviewed'}).string   # 电影名
            movieInfo.append(moviename)

            parse_list11 = [st for st in Infoareaoneone.stripped_strings]  # 爬取第一部分第一区域
            for i in parse_list11:
                if i == '/':
                    parse_list11.remove(i)
                elif i == ':':
                    parse_list11.remove(i)
            a = {'导演': 'none', '编剧': 'none', '主演': 'none', '类型': 'none', '官方网站': 'none', '制片国家/地区': 'none',
                 '语言': 'none', '上映日期': 'none', '片长': 'none', '又名': 'none', 'IMDb链接': 'none'}
            for i in range(len(parse_list11)):
                if parse_list11[i] == '导演':
                    a['导演'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '编剧':
                    a['编剧'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '主演':
                    a['主演'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '类型:':
                    a['类型'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '官方网站:':
                    a['官方网站'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '制片国家/地区:':
                    a['制片国家/地区'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '语言:':
                    a['语言'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '上映日期:':
                    a['上映日期'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '片长:':
                    a['片长'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == '又名:':
                    a['又名'] = i
            for i in range(len(parse_list11)):
                if parse_list11[i] == 'IMDb链接:':
                    a['IMDb链接'] = i

            b = []  # 存储a中value为数字的值
            for key in a:
                if a[key] != 'none':
                    b.append(a[key])

            c = 0  # 初始设为0
            if a['导演'] == 'none':  # 导演
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['导演']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['导演'] + 1:c]))

            if a['编剧'] == 'none':  # 编剧
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['编剧']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['编剧'] + 1:c]))

            if a['主演'] == 'none':  # 主演
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['主演']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['主演'] + 1:c]))

            if a['类型'] == 'none':  # 类型
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['类型']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['类型'] + 1:c]))

            if a['官方网站'] == 'none':  # 官方网站
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['官方网站']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['官方网站'] + 1:c]))

            if a['制片国家/地区'] == 'none':  # 制片国家/地区
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['制片国家/地区']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['制片国家/地区'] + 1:c]))

            if a['语言'] == 'none':  # 语言
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['语言']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['语言'] + 1:c]))

            if a['上映日期'] == 'none':  # 上映日期
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['上映日期']:
                        c = i
                        break
                movieInfo.append('/'.join(parse_list11[a['上映日期'] + 1:c]))

            if a['片长'] == 'none':  # 片长
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['片长']:
                        c = i
                        movieInfo.append('/'.join(parse_list11[a['片长'] + 1:c]))
                        break
                if a['片长'] == c:
                    movieInfo.append('/'.join(parse_list11[a['片长'] + 1:]))

            if a['又名'] == 'none':  # 又名
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['又名']:
                        c = i
                        movieInfo.append('/'.join(parse_list11[a['又名'] + 1:c]))
                        break
                if a['又名'] == c:
                    movieInfo.append('/'.join(parse_list11[a['又名'] + 1:]))

            if a['IMDb链接'] == 'none':  # IMDb链接
                movieInfo.append('none')
            else:
                for i in b:
                    if i > a['IMDb链接']:
                        c = i
                        movieInfo.append('/'.join(parse_list11[a['IMDb链接'] + 1:c]))
                        break
                if a['IMDb链接'] == c:
                    movieInfo.append('/'.join(parse_list11[a['IMDb链接'] + 1:]))

            parse_list12 = [st for st in Infoareaonetwo.stripped_strings]  # 爬取第一部分第二区域
            for i in parse_list12:
                if i == '好于':
                    parse_list12.remove(i)
            movieInfo.append(parse_list12[2])  # 总评分
            movieInfo.append(parse_list12[3])  # *人评价
            movieInfo.append(parse_list12[6])  # 5星
            movieInfo.append(parse_list12[8])  # 4星
            movieInfo.append(parse_list12[10])  # 3星
            movieInfo.append(parse_list12[12])  # 2星
            movieInfo.append(parse_list12[14])  # 1星
            movieInfo.append('/'.join(parse_list12[15:]))  # 好于

            parse_list2 = [st for st in Infoareatwo.stripped_strings]       # 爬取第二部分
            for i in parse_list2:
                if i == '/':
                    parse_list2.remove(i)
            movieInfo.append(parse_list2[0])        # *人看过
            movieInfo.append(parse_list2[1])        # *人想看
            print(movieInfo)
            f.writelines(','.join(map(str, movieInfo))+'\n')
        except:
            print('失败')
            f.writelines('\n')
    f.close()


def main():
    lists = []
    rect = ['影片','导演','编剧','主演','类型','官方网站','制片国家/地区','语言','上映日期','片长','又名','IMDb链接',
            '总评价','*人评价','5星','4星','3星','2星','1星','好于','看过', '想看']
    path = 'D://MovieList.csv'
    movieurl = getMovieUrl(lists)
    movieurl = list(set(movieurl))
    file_movie_id = open('D://file_movie_id.txt', 'w')
    file_movie_id.writelines(','.join(movieurl))
    file_movie_id.close()
    print(movieurl)
    getMovieInfo(movieurl, path, rect)


main()