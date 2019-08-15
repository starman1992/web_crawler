import urllib.request as r
import re
import os

def open_url(url):
    req = r.Request(url)   
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36\
                    (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    response = r.urlopen(req)
    html = response.read().decode('utf-8')
    return html

def get_imgs(url):
    p = r'<img class="pic-large" src="([^"]+\.jpg)"'
    img_addrs = re.findall(p,url)
    for each in img_addrs:
        print('已保存' + each)

    for each in img_addrs:
        filename = each.split('/')[-1]
        r.urlretrieve(each,filename,None)


def savepic(folder='风景'):
    os.chdir('C:\\Users\\WXYZ\\Desktop')
    os.makedirs(folder,exist_ok=True)
    os.chdir(folder)

    for page in range(1,10):
        url = f'http://www.win4000.com/wallpaper_detail_160341_{page}.html'
        print(url)
        get_imgs(open_url(url))

if __name__ == '__main__':
    savepic()
        











