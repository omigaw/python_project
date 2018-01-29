# -*- coding: utf-8 -*-
import requests
import time
import random
import re
from bs4 import BeautifulSoup

f = open('D://file_movie_id.txt')
list = f.read().strip(',').split(',')
f.close()

urlclick = 'https://movie.douban.com/subject/{}/'

cookies123={'Cookie':'ll="108288"; bid=QPeyJBpC844; ps=y; gr_user_id=b9272825-9a9d-408f-9dba-7c89201f297b; viewed="26986954_27113800"; __yadk_uid=29ZMYqosbOucBaTmQFo7OZD42ebN6kKU; ap=1; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=E11A9229BB62B9B4E38D2928E3025A98|92cdb5c62c8bed591ca0ab9bd495257a; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1516860707%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3Dba14c11545b73c28%26alias%3D%22%5D; __utmt=1; _gat_UA-7019765-1=1; ck=7JgX; _pk_id.100001.8cb4=9600cea801cc837d.1516591535.10.1516860751.1516848962.; _pk_ses.100001.8cb4=*; __utma=30149280.1796725684.1516029981.1516843691.1516860708.21; __utmb=30149280.2.10.1516860708; __utmc=30149280; __utmz=30149280.1516843691.20.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17294; _ga=GA1.2.1796725684.1516029981; _gid=GA1.2.910259410.1516794568; dbcl2="172948998:g4AffHShwsM"'}
cookies_a={'Cookie':'ll="108288"; bid=t85sQYa0ZPc; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1516797000%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DUq7tQkNb11H1ZrsCpkkw0h-Ojcz6CmjF6E-mDuAHdyJv-mbZkYguzx-EVwyQFAX6%26wd%3D%26eqid%3Dc934d92100055318000000035a687c42%26ck%3D0.0.0.0.0.0.0.0%26shh%3Dwww.baidu.com%26sht%3Dbaidu%22%5D; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.8cb4=5e776350485e535e.1516797000.1.1516799847.1516797000.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.875741024.1516797002.1516797002.1516797002.1; __utmb=30149280.21.10.1516797002; __utmc=30149280; __utmz=30149280.1516797002.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17304; _ga=GA1.2.875741024.1516797002; _gid=GA1.2.628834483.1516797028; _gat_UA-7019765-1=1; dbcl2="138938893:Y4XdRZFfI8c"'}

def getHTMLText(url, code='utf-8'):
    try:
        time.sleep(random.randint(1, 3))
        kv = {'user-agent': 'Mozilla/5.0'}
        proxies = {'http': 'http://117.36.103.170:8118'}
        r = requests.get(url, headers=kv, timeout=30, proxies=proxies, cookies=cookies123)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "没有返回信息"


def getMovieInfo(movieurl, fpath, rect):
    f = open(fpath, 'a')
    # f.writelines(','.join(rect)+'\n')
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
                        movieInfo.append('.'.join('/'.join(parse_list11[a['又名'] + 1:c]).split(',')))
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
    rect = ['影片', '导演', '编剧', '主演', '类型', '官方网站', '制片国家/地区', '语言', '上映日期', '片长', '又名', 'IMDb链接',
            '总评价', '*人评价', '5星', '4星', '3星', '2星', '1星', '好于', '看过', '想看']
    path = 'D://MovieList_400onetime.csv'
    getMovieInfo(list[6680:], path, rect)


main()
