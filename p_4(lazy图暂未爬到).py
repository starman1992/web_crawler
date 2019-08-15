import urllib.request as r
import os
import re
import requests

def open_url(url):
    req = r.Request(url)   
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36\
                    (KHTML, like Gecko) Chrome/68.0.344.106 Safari/537.36')
    response = r.urlopen(req)
    html = response.read().decode('utf-8')
    with open('test.txt','w+',encoding='utf-8') as f:
        f.write(html)
    
    return html

def get_imgs(url):
    p = r'<img src="([^"]+\.jpg)"'
    img_addrs = re.findall(p,url)
    header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/68.0.344.106 Safari/537.36'}
    for each in img_addrs: 
        filename = each.split('/')[-1]
        #r.urlretrieve(each,filename,None)
        #r = requests.get(each,headers=header)
        with open(filename,'wb') as f:
            f.write(requests.get(each,headers=header).content)
        print('已保存' + str(each)) 

def savepic(folder='美女test2'):
    os.chdir('C:\\Users\\WXYZ\\Desktop')
    os.makedirs(folder,exist_ok=True)
    os.chdir(folder)

    
    for page in range(1,2):
        url = f'https://www.mzitu.com/124109/{page}'
        print(url)
        get_imgs(open_url(url))    

if __name__ == '__main__':
    savepic()
        











