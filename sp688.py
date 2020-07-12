#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import uuid
import shutil
session = requests.Session()


def getImages(pageUrl,folder):
    pageResp = session.get(pageUrl)
    pageResp.encoding = pageResp.apparent_encoding
    pageSoup = BeautifulSoup(pageResp.text, features='lxml')
    pageTarget = pageSoup.find(attrs={"class":"img-wrapper"})
    
    img_url = pageTarget.find("img").attrs.get("src").strip('//')
    img_type = img_url.split('.')[-1]
    img_name = img_url.split('.')[-2].split('/')[-1]

    with open(os.path.join(folder,  img_name + str(uuid.uuid4())+'.'+img_type),'wb') as f:
        if("https" not in img_url):
                img_url = "https://"+img_url
        imgResp = session.get(url=img_url)
        imgResp.encoding = imgResp.apparent_encoding
        print(img_name+str(imgResp.status_code))
        f.write(imgResp.content)



def getPages(folder, url):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    resp = session.get(url)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, features='lxml')
    allLi = soup.find(attrs={"class":"image-list current-list fd-clr"}).find("ul").find_all("li")
    allPages = list()
    for li in allLi :
        a = li.find("a")
        allPages.append(a.attrs.get("href"))
        with open(os.path.join(folder,folder+".txt"),'a') as f:
            f.writelines("\n"+a.attrs.get("href"))

    for page in allPages:
        getImages(page,folder)

def runDownLoadShopImage(configFile):
    idx = 1
    with open(configFile,"r") as f:
        for item in f:
            getPages(str(idx),item)
            idx+=1

runDownLoadShopImage("target_shop.txt")
