#取猫图
import urllib.request

def savepic(wideth,height):
    url = f'http://placekitten.com/g/{wideth*100}/{height*100}'
    response = r.urlopen(url)
    cat_img = response.read()

    with open(f'cat_{wideth*100}_{height*100}.jpg','wb') as f:
        f.write(cat_img)


for n in range(1,10):
    savepic(n,n)











