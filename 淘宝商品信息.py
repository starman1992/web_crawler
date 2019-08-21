'''
本代码的关键信息在于添加访问淘宝的头部信息，最重要的就是cookie
方法是：
在淘宝登录后任意搜索一个商品
F12-Network-All-(找到有cookie的Request Header)
对该链接Name属性下，Copy as curl(bash)
用https://curl.trillworks.com/网址翻译为python语言
只需提取出Headers，复制Headers，插入变量（把'个人昵称'改为个人昵称）
最后在rquests.get()中添加header值就行了

#待添加链接
'''
import requests as rq
import pandas as pd
import re 

def getHTMLText(url):
    try:
        header = {
            'authority': 'www.taobao.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.2740.106 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E4%B9%A6%E5%8C%85&suggest=history_1&_input_charset=utf-8&wq=shub&suggest_query=shub&source=suggest',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; miid=1843928429766405102; cna=CDayDhKTbVwCAXRNCvU7OBGJ; enc=Ko7nvTVHfDTfTB4c75NbRCcpEV%2BjqUFcO49TKHIXj1xqE3rdRQPV%2FDoE4DRltD5DRVndGbS1MRSnN%2FuXKDic5w%3D%3D; tracknick=个人昵称; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; t=ed47d54e82452f2ec6856f1e5c005090; UM_distinctid=16ab400a280403-063718f8b9a8f9-43480420-100200-16ab400a281519; lgc=个人昵称; _m_h5_tk=f9b3c4dc27d3c0c8efec38d22f6c1989_1566312488120; _m_h5_tk_enc=b69adce9de8c68fa18e9e29351cd1d8c; v=0; cookie2=1246eeb22c6981000692cc79931f0613; _tb_token_=ef3deb6e8ffee; unb=2003827157; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dBy3K7lX13XxUOq8Y%3D&id2=UUjRIbDCcQ6ocg%3D%3D&nk2=BJf2REDkJrTR0Ls%3D; csg=652a635e; cookie17=UUjRIbDCcQ6ocg%3D%3D; dnk=个人昵称; skt=30728106b277e9be; existShop=MTU2NjM1MTY3NA%3D%3D; uc4=id4=0%40U2ozluC1B0M6CVMz7op6u7ZkVNa5&nk4=0%40BpM%2F5iL9ggcenT7S%2FCfEp2szgNnPWQ%3D%3D; _cc_=UtASsssmfA%3D%3D; _l_g_=Ug%3D%3D; sg=g70; _nk_=个人昵称; cookie1=UoTcDqR0cXCKlbbQiZ%2FN7ZSs5K81YbYPwmciurU2Ls4%3D; mt=ci=10_1; whl=-1%260%260%261566351684480; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=UIHiLt3xThH8t7YQouiW&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTaHoguciZyzg%3D%3D&cart_m=0&tag=10&lng=zh_CN; isg=BOfnylendqKkxfgEIrCCbzpFdhtxxMNFVDyBX7lUA3adqAdqwTxLniWqyuiTW5PG; l=cBS5MXCrvzYdLnV2BOCanurza77OSIRYYuPzaNbMi_5d26T6qS_OkJLIWF96VjWd9CTB42FvhwJ9-etkZ2rfdFK-g3fP.',
            'if-none-match': 'W/"2b87-1602480f459"',
            }
        r = rq.get(url,headers=header,timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
##        print(r.text)
        return r.text
    except:
        return ""

def parsePage(ItemList,html):
    titleList = re.findall(r'"raw_title":"(.*?)"',html)
    priceList = re.findall(r'"view_price":"([\d.]*?)"',html)
    locList = re.findall(r'"item_loc":"(.*?)"',html)
    salesList = re.findall(r'"view_sales":"(\d.*?)"',html)
    commList = re.findall(r'"comment_count":"(\d*?)"',html)
    nickList = re.findall(r'"nick":"(.*?)"',html)
##    ItemList = [list(i) for i in list(zip(priceList,titleList))]
##    不能用该式子，因为是函数内临时性zip，出了该def无效赋值
    
    for i in range(len(priceList)):
        ItemList.append([priceList[i],titleList[i],locList[i],salesList[i],commList[i],nickList[i]])
##        print('\r当前进度:{:.2f}%'.format(i*100/len(priceList)),end='')
##    print(ItemList[0])
       
def printItemList(ItemList):
##    print(ItemList)
    tplt = '{:4}\t{:8}\t{:16}\t{:6}\t{:4}\t{:4}\t{:4}'
    print(tplt.format('序号','价格','商品名','地址','付款人数','评论数','店名'))
    count = 0
    for i in ItemList:
        count += 1
        print(tplt.format(count,i[0],i[1],i[2],i[3],i[4],i[5]))
        
def write(tlist,ItemList,filename):
    # list转dataframe
    count = 0
    for i in range(len(ItemList)):
        count += 1
        ItemList[i].insert(0,count)
    df = pd.DataFrame(ItemList, columns=tlist)
    # 保存到本地excel
    df.to_excel(filename, index=False)
    
def main():
    goods = input('请输入你要搜索的商品：')
    start_url = 'https://s.taobao.com/search?q=' + goods
    filename = ("淘宝商品信息_%s.xlsx" % goods)
    print(filename)
    infoList = []
    for page in range(2):
        url = start_url + '&s=' + str(44*page)
        html = getHTMLText(url)
        parsePage(infoList,html)
##    printItemList(infoList)
    tlist=['序号','价格','商品名','地址','付款人数','评论数','店名']
    write(tlist,infoList,filename)
    print('已下载'+str(filename))
        

if __name__ == '__main__':
    main()

   











