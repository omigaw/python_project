# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
###################################### 说明  ####################################
#                    爬取2000-2015段30000多电影数据的cast&crew
#################################################################################
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

    res = ['movieid', 'moviename', 'director', 'writing credits (WGA)', 'WGA_detail', 'nameid','cast (fist 10)','nameid'
        ,'produced by','producer_detail','cinematograph','cinema detail','nameid','film edit','nameid','casting','nameid'
        ,'production design','nameid','art direction','nameid','production management','detail','nameid','second unit director or assistant director',
         'detail','nameid','special effect','detail','nameid','visual effect','detail','nameid']
    f = open(fpath, 'w')
    f.writelines(','.join(res) + '\n')

    for film in lst:
        url = 'http://www.imdb.com/title/'+film+'/fullcredits?ref_=tt_cl_sm#cast'
        html = getHTMLText(url)
        count +=1
        res[0] = film                                 # movieid

        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, 'html.parser')  # 煲汤
            allInfo = soup.find('div', attrs={'class': 'article listo'})       # 爬虫主体
            res[1] = allInfo.find('div', attrs={'class': 'parent'}).find('h3',attrs={'itemprop': 'name'}).find('a').string.replace("\n","").replace(",",".")             # moviename

        # 主体
            mainInfo = allInfo.find('div',attrs={'id':'fullcredits_content','class':'header'})
            theads = mainInfo.find_all('h4',attrs = {'class':'dataHeaderWithBorder'})
            tbodys = mainInfo.find_all('table')
            arrayThead = {}
            index = 0
            arrayTbody = []
            for thead in theads:
                arrayThead[''.join(map(str,thead.stripped_strings))]=index
                index +=1
                # print(''.join(map(str,thead.stripped_strings)))

            strDirec = ""
            if "Directed by" in arrayThead.keys():
                directors = tbodys[arrayThead.get("Directed by")].find_all('td',attrs={'class':'name'}) # director
                for director in directors:
                    strDirec = strDirec + director.find('a').string.replace(",","|").strip()
                    strDirec = strDirec+'|'
                res[2] = strDirec.rstrip('|').encode('utf-8')

            else:
                res[2] = ""

            strWrit = ""                                                                 # Writing Credits
            strDetail = ""
            strNameId = ""
            if "Writing Credits" in arrayThead.keys():
                writers = tbodys[arrayThead.get("Writing Credits")].find_all('td',attrs={'class':'name'})
                for writer in writers:
                    strWrit = strWrit + writer.find('a').string.strip()
                    strWrit = strWrit+'|'
                    strNameId = strNameId + writer.find('a').attrs['href'].split("/")[2]
                    strNameId = strNameId +'|'
                res[3] = strWrit.rstrip('|').encode('utf-8')
                res[5] = strNameId.rstrip('|').encode('utf-8')

                writer_details = tbodys[arrayThead.get("Writing Credits")].find_all('td',attrs={'class':'credit'})
                for detail in writer_details:
                    if len(detail.string)>0:
                        strDetail = strDetail + detail.string.replace(",",".").strip()
                        strDetail = strDetail + '|'
                    else:
                        strDetail = strDetail+ "None"
                        strDetail = strDetail+'|'
                res[4] = strDetail.rstrip('|').encode('utf-8')


            elif "Writing Credits(WGA)" in arrayThead.keys():
                writers = tbodys[arrayThead.get("Writing Credits(WGA)")].find_all('td', attrs={'class': 'name'})
                for writer in writers:
                    strWrit = strWrit + writer.find('a').string.strip()
                    strWrit = strWrit + '|'
                    strNameId = strNameId + writer.find('a').attrs['href'].split("/")[2]
                    strNameId = strNameId + '|'
                res[3] = strWrit.rstrip('|').encode('utf-8')
                res[5] = strNameId.rstrip('|').encode('utf-8')
                writer_details = tbodys[arrayThead.get("Writing Credits(WGA)")].find_all('td', attrs={'class': 'credit'})
                for detail in writer_details:
                    if len(detail.string) > 0:
                        strDetail = strDetail + detail.string.replace(",", ".").strip()
                        strDetail = strDetail + '|'
                    else:
                        strDetail = strDetail + "None"
                        strDetail = strDetail + '|'
                res[4] = strDetail.rstrip('|').encode('utf-8')


            else:
                res[3] = ""
                res[4] = ""
                res[5] = ""

            strCasName = ""
            strCasId = ""
            if len(mainInfo.find('table',attrs={'class':'cast_list'}))>0 :
                castList = mainInfo.find('table',attrs={'class':'cast_list'})
                casts = castList.find_all('tr')
                for inde in range(10):
                    casTwoInfo = casts[inde+1].find_all('td')[1].find('a')
                    strCasName = strCasName + casTwoInfo.string.strip()       # name
                    strCasName = strCasName + '|'
                    strCasId = strCasId+casTwoInfo.attrs['href'].split("/")[2]     # nameId
                    strCasId = strCasId + '|'
                res[6] = strCasName.rstrip('|').encode('utf-8')
                res[7] = strCasId.rstrip('|').encode('utf-8')
            else:
                res[6]=""
                res[7]=""

            strProdu = ""
            strProDetai = ""
            if "Produced by" in arrayThead.keys():
                producers = tbodys[arrayThead.get("Produced by")].find_all('td', attrs={'class': 'name'})
                for producer in producers:
                    strProdu = strProdu + producer.find('a').string.strip()
                    strProdu = strProdu + '|'
                res[8] = strProdu.rstrip('|').encode('utf-8')              # produced by

                produDs = tbodys[arrayThead.get("Produced by")].find_all('td', attrs={'class': 'credit'})
                for produD in produDs:
                    if len(produD.string)>0:
                        strProDetai = strProDetai + produD.string.replace(",",".").strip()
                        strProDetai = strProDetai + '|'
                    else:
                        strProDetai = strProDetai + "None"
                        strProDetai = strProDetai + '|'
                res[9] = strProDetai.rstrip('|').encode('utf-8')             # producer detail
            else:
                res[8] = ""
                res[9] = ""

            strCinemato =""                                         # cinematograph
            strCineId = ""
            strCineDetai = ""
            if "Cinematography by" in arrayThead.keys():
                Cinematos = tbodys[arrayThead.get("Cinematography by")].find_all('td', attrs={'class': 'name'})
                for cinemato in Cinematos:
                    strCinemato = strCinemato + cinemato.find('a').string.strip()
                    strCinemato = strCinemato + '|'
                    strCineId = strCineId + cinemato.find('a').attrs['href'].split("/")[2]
                    strCineId = strCineId + '|'
                res[10] = strCinemato.rstrip('|').encode('utf-8')
                res[12] = strCineId.rstrip('|').encode('utf-8')                       # nameid

                cinema_details = tbodys[arrayThead.get("Cinematography by")].find_all('td', attrs={'class': 'credit'})
                for cdetail in cinema_details:
                    if len(cdetail.string) > 0:
                        strCineDetai = strCineDetai + detail.string.replace(",", ".").strip()
                        strCineDetai = strCineDetai + '|'
                    else:
                        strCineDetai = strCineDetai + "None"
                        strCineDetai = strCineDetai + '|'
                res[11] = strCineDetai.rstrip('|').encode('utf-8')
            else:
                res[10] = ""
                res[11] = ""
                res[12] = ""

            strFilmEdit = ""                                                     # film edit
            strFilEdiName = ""
            if "Film Editing by" in arrayThead.keys():
                FilmEdits = tbodys[arrayThead.get("Film Editing by")].find_all('td', attrs={'class': 'name'})
                for filmEdit in FilmEdits:
                    strFilmEdit = strFilmEdit + filmEdit.find('a').string.strip()
                    strFilmEdit = strFilmEdit + '|'
                    strFilEdiName = strFilEdiName + filmEdit.find('a').attrs['href'].split("/")[2]
                    strFilEdiName = strFilEdiName + '|'
                res[13] = strFilmEdit.rstrip('|').encode('utf-8')
                res[14] = strFilEdiName.rstrip('|').encode('utf-8')                     # nameid
            else:
                res[13]=""
                res[14]=""

            strCasting = ""                                                  # casting
            strCastingName = ""
            if "Casting By" in arrayThead.keys():
                Castings = tbodys[arrayThead.get("Casting By")].find_all('td', attrs={'class': 'name'})
                for casting in Castings:
                    strCasting = strCasting + casting.find('a').string.strip()
                    strCasting = strCasting + '|'
                    strCastingName = strCastingName + casting.find('a').attrs['href'].split("/")[2]
                    strCastingName = strCastingName + '|'
                res[15] = strCasting.rstrip('|').encode('utf-8')
                res[16] = strCastingName.rstrip('|').encode('utf-8')                   # nameid
            else:
                res[15] = ""
                res[16] = ""

            strProducDesign  = ""                                            # production design
            strProducDeName = ""
            if "Production Design by" in arrayThead.keys():
                ProDesigns = tbodys[arrayThead.get("Production Design by")].find_all('td', attrs={'class': 'name'})
                for prodesign in ProDesigns:
                    strProducDesign = strProducDesign + prodesign.find('a').string.strip()
                    strProducDesign = strProducDesign + '|'
                    strProducDeName = strProducDeName + prodesign.find('a').attrs['href'].split("/")[2]
                    strProducDeName = strProducDeName + '|'
                res[17] = strProducDesign.rstrip('|').encode('utf-8')
                res[18] = strProducDeName.rstrip('|').encode('utf-8')  # nameid
            else:
                res[17] = ""
                res[18] = ""

            strArtDirection = ""  # art direction
            strArtDirecName = ""
            if "Art Direction by" in arrayThead.keys():
                Arts = tbodys[arrayThead.get("Art Direction by")].find_all('td', attrs={'class': 'name'})
                for art in Arts:
                    strArtDirection = strArtDirection + art.find('a').string.strip()
                    strArtDirection = strArtDirection + '|'
                    strArtDirecName = strArtDirecName + art.find('a').attrs['href'].split("/")[2]
                    strArtDirecName = strArtDirecName + '|'
                res[19] = strArtDirection.rstrip('|').encode('utf-8')
                res[20] = strArtDirecName.rstrip('|').encode('utf-8')  # nameid
            else:
                res[19] = ""
                res[20] = ""

            strProducMana = ""                            # production management
            strProManDetail = ""
            strProManName = ""
            if "Production Management" in arrayThead.keys():
                ProducManags = tbodys[arrayThead.get("Production Management")].find_all('td', attrs={'class': 'name'})
                for producMana in ProducManags:
                    strProducMana = strProducMana + producMana.find('a').string.strip()
                    strProducMana = strProducMana + '|'
                    strProManName = strProManName + producMana.find('a').attrs['href'].split("/")[2]
                    strProManName = strProManName + '|'
                res[21] = strProducMana.rstrip('|').encode('utf-8')
                res[23] = strProManName.rstrip('|').encode('utf-8')

                proMan_details = tbodys[arrayThead.get("Production Management")].find_all('td', attrs={'class': 'credit'})
                for pro_detail in proMan_details:
                    if len(pro_detail.string) > 0:
                        strProManDetail = strProManDetail + pro_detail.string.replace(",", ".").strip()
                        strProManDetail = strProManDetail + '|'
                    else:
                        strProManDetail = strProManDetail + "None"
                        strProManDetail = strProManDetail + '|'
                res[22] = strProManDetail.rstrip('|').encode('utf-8')
            else:
                res[21]=""
                res[22] = ""
                res[23] = ""

            strSUDOAD = ""                        # second unit director or assistant director
            strSUDOADDetail = ""
            strSUDOADName = ""
            if "Second Unit Director or Assistant Director" in arrayThead.keys():
                SUDOADs = tbodys[arrayThead.get("Second Unit Director or Assistant Director")].find_all('td', attrs={'class': 'name'})
                for sudoad in SUDOADs:
                    strSUDOAD = strSUDOAD + sudoad.find('a').string.strip()
                    strSUDOAD = strSUDOAD + '|'
                    strSUDOADName = strSUDOADName + sudoad.find('a').attrs['href'].split("/")[2]
                    strSUDOADName = strSUDOADName + '|'
                res[24] = strSUDOAD.rstrip('|').encode('utf-8')
                res[26] = strSUDOADName.rstrip('|').encode('utf-8')

                sudoad_details = tbodys[arrayThead.get("Second Unit Director or Assistant Director")].find_all('td',
                                                                                          attrs={'class': 'credit'})
                for sudoad_detail in sudoad_details:
                    if len(sudoad_detail.string) > 0:
                        strSUDOADDetail = strSUDOADDetail + sudoad_detail.string.replace(",", ".").strip()
                        strSUDOADDetail = strSUDOADDetail + '|'
                    else:
                        strSUDOADDetail = strSUDOADDetail + "None"
                        strSUDOADDetail = strSUDOADDetail + '|'
                res[25] = strSUDOADDetail.rstrip('|').encode('utf-8')
            else:
                res[24] = ""
                res[25] = ""
                res[26] = ""

            strSpeciEffect = ""                            # special effect
            strSpecEffecDetail = ""
            strSpecEffeName = ""
            if "Special Effects by" in arrayThead.keys():
                specEffects = tbodys[arrayThead.get("Special Effects by")].find_all('td', attrs={
                    'class': 'name'})
                for specEffect in specEffects:
                    strSpeciEffect = strSpeciEffect + specEffect.find('a').string.strip()
                    strSpeciEffect = strSpeciEffect + '|'
                    strSpecEffeName = strSpecEffeName + specEffect.find('a').attrs['href'].split("/")[2]
                    strSpecEffeName = strSpecEffeName + '|'
                res[27] = strSpeciEffect.rstrip('|').encode('utf-8')
                res[29] = strSpecEffeName.rstrip('|').encode('utf-8')

                specEffect_details = tbodys[arrayThead.get("Special Effects by")].find_all('td',attrs={'class': 'credit'})

                for specEff_detail in specEffect_details:
                    if len(specEff_detail.string) > 0:
                        strSpecEffecDetail = strSpecEffecDetail + specEff_detail.string.replace(",", ".").strip()
                        strSpecEffecDetail = strSpecEffecDetail + '|'
                    else:
                        strSpecEffecDetail = strSpecEffecDetail + "None"
                        strSpecEffecDetail = strSpecEffecDetail + '|'
                res[28] = strSpecEffecDetail.rstrip('|').encode('utf-8')
            else:
                res[27] = ""
                res[28] = ""
                res[29] = ""

            strVisualEffect = ""                        # visual effect
            strVisualEffecDetail = ""
            strVisualEffeName = ""
            if "Visual Effects by" in arrayThead.keys():
                visualEffects = tbodys[arrayThead.get("Visual Effects by")].find_all('td', attrs={
                    'class': 'name'})
                for visuEffect in visualEffects:
                    strVisualEffect = strVisualEffect + visuEffect.find('a').string.strip()
                    strVisualEffect = strVisualEffect + '|'
                    strVisualEffeName = strVisualEffeName + visuEffect.find('a').attrs['href'].split("/")[2]
                    strVisualEffeName = strVisualEffeName + '|'
                res[30] = strVisualEffect.rstrip('|').encode('utf-8')
                res[32] = strVisualEffeName.rstrip('|').encode('utf-8')

                visualEffect_details = tbodys[arrayThead.get("Visual Effects by")].find_all('td',
                                                                                           attrs={'class': 'credit'})

                for visual_detail in visualEffect_details:
                    if len(visual_detail.string) > 0:
                        strVisualEffecDetail = strVisualEffecDetail + visual_detail.string.replace(",", ".").strip()
                        strVisualEffecDetail = strVisualEffecDetail + '|'
                    else:
                        strVisualEffecDetail = strVisualEffecDetail + "None"
                        strVisualEffecDetail = strVisualEffecDetail + '|'
                res[31] = strVisualEffecDetail.rstrip('|').encode('utf-8')
            else:
                res[30] = ""
                res[31] = ""
                res[32] = ""
            f.writelines(','.join(map(str, res)) + '\n')
        except:
            print(res[0])
            continue
        print(res)
        print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
    f.close()

def main():
    # output_file = 'D://dictionary.txt'
    output_file1 = 'E://cast.csv'
    alist = []
    getActorList(alist)
    print("length of alist:")
    print(len(alist))

    getAwardInfo(alist, output_file1)
    # print(len(infoDict))


main()
