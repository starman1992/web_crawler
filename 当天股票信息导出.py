import requests as rq
import pandas as pd
from bs4 import BeautifulSoup
import re
import os

def getHTMLText(url,code='utf-8'):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/68.1.3440.106 Safari/537.36'}
        r = rq.get(url,headers=header,timeout = 30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def getStockList(ItemList,html):
    html = getHTMLText(html,'GB2312')
    soup = BeautifulSoup(html,'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            ItemList.append(re.findall(r'sh60\d{4}',href)[0])
            #findall生成的是一个列表类型
            #或用ItemList.append(re.search(r'[s][hz]\d{6}',href).group(0))
        except:
            continue
    
       
def getStockInfo(ItemList,stockURL,fpath,ItemDictList):
    count = 0
    for stock in ItemList:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == "":
                continue     #东方财富的股票码可能在百度网页中没有
            infoDict = {}
            soup = BeautifulSoup(html,'html.parser')
            #以下给予了两种方法返回tag格式，.find和.find_all或直接加括号后面取列表元素
            #find_all返回的是列表格式，find返回的是tag格式
            stockInfo = soup.find('div',attrs = {'class':'stock-bets'})
            name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
            #.text和.string区别在于：
            #1.没有子标签，且有文本时，两者的返回结果一致，都是文本
            #2.没有子标签，且没有文本时，.string返回None，.text返回为空
            #3.只有一个子标签时，且文本只出现在子标签之间时，两者返回结果一致，都返回子标签内的文本
            #4.就是我们这里讲解的例子！有子标签，并且父标签td和子标签span各自包含一段文本时。string返回None，text返回父标签和子标签的文本
            infoDict.update({'股票名称':name.text.split()[0]+name.text.split()[1]})   #宏大爆破 002683
            keyList = stockInfo('dt')
            valueList = stockInfo('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val
##            print(infoDict)
##            writetxt(fpath,infoDict)            
        except:
            count += 1
##            print('\r当前进度:{:.2f}%'.format(count*100/len(ItemList)),end='')
            continue
        ItemDictList.append(infoDict)
        count += 1
        print('\r当前进度:{:.2f}%'.format(count*100/len(ItemList)),end='')
        
def writetxt(fpath,stodict):
    with open(fpath,'a',encoding = 'utf-8') as f:
        f.write(str(infoDict) + '\n')
        count += 1
##        print('\r当前进度:{:.2f}%'.format(count*100/len(ItemList)),end='')


def writeexcel(fpath,ItemDictList):
    # list转dataframe
    df = pd.DataFrame(ItemDictList)
    # 保存到本地excel
    df.to_excel(fpath, index=False)
    
def main():
    os.chdir('C:/Users/WXYZ/Desktop')
    stock_list_url = 'http://quote.eastmoney.com/stock_list.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    filename1 = '股票信息.txt'
    filename2 = '股票信息.xlsx'
    slist = []
    stockDictList = []
    getStockList(slist,stock_list_url)
    getStockInfo(slist,stock_info_url,filename1,stockDictList)
    writeexcel(filename2,stockDictList)
##    print('已下载'+str(filename))
        
if __name__ == '__main__':
    main()

   











