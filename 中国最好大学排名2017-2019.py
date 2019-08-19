import requests as rq
from bs4 import BeautifulSoup
import bs4
import pandas as pd

def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        r = rq.get(url,kv,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def filltitleList(tlist,html):
    soup = BeautifulSoup(html,'html.parser')
    for th in soup.find('thead').descendants:
        if isinstance(th,bs4.element.Tag) and th.string != None:
            tlist.append(th.string)
##    print(len(tlist))

def fillUnivList(ulist,html,num):
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.prettify())
##    for tr in soup.find('tbody').children:
##        if isinstance(tr,bs4.element.Tag):
##            tds = tr('td')
##            ulist.append([tds[0].string,tds[1].string,tds[3].string])
    for tr in soup.find_all('tr',attrs={'class':'alt'}):
        tds = tr('td')
        oneunv = []
        for i in range(num):#16-17年是13组，18-19年是14组
            oneunv.append(tds[i].string)
        ulist.append(oneunv)   #ulist是二维数组
            
def printUnivList(ulist,tlist,top):
    tplt = '{0:<6}\t{1:{4}^10}\t{2:^10}\t{3:^6}'
    print(tplt.format('排名','学校','省市','总分',chr(12288)))
    for i in range(top):
        u=ulist[i]
        print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))
        
def write(tlist,ulist,filename):
    # list转dataframe
    df = pd.DataFrame(ulist, columns=tlist)
    # 保存到本地excel
    df.to_excel(filename, index=False)

def main():
    for year in range(2016,2020):#15年的编码奇怪
        uinfo = []
        tinfo = []
        url = f'http://www.zuihaodaxue.com/zuihaodaxuepaiming{year}.html'
        filename=f"中国最好大学排名{year}.xlsx"
        html = getHTMLText(url)
        filltitleList(tinfo,html)
        fillUnivList(uinfo,html,num=len(tinfo))
        write(tinfo,uinfo,filename)
        print('已下载 '+str(filename))
    ##    printUnivList(uinfo,tinfo,20)
        
if __name__ == '__main__':
    main()

   











