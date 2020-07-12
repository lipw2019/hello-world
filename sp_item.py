#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import uuid
import shutil
session = requests.Session()




def downloadImage(img_url, folder):
    img_type = img_url.split('.')[-1]
    img_name = img_url.split('.')[-2].split('/')[-1]
    with open(os.path.join(folder,  img_name + str(uuid.uuid4())+'.'+img_type),'wb') as f:
        if("https" not in img_url):
                img_url = "https://"+img_url
        imgResp = session.get(url=img_url)
        imgResp.encoding = imgResp.apparent_encoding
        f.write(imgResp.content)

def getPageImages(folder, url):

    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    pageResp = session.get(url)
    pageResp.encoding = pageResp.apparent_encoding
    pageSoup = BeautifulSoup(pageResp.text, features='lxml')
    print(pageSoup)

    allLi = pageSoup.find(attrs={"class":"tab-nav-container"}).find_all("li")
    allImages = list()
    for li in allLi:
        strAddr = li.attrs.get("data-img")
        with open(os.path.join(folder,folder+".txt"),'a') as f:
            f.writelines("\n"+strAddr)
        downloadImage(strAddr, folder)
    print(allImages)



def runDownLoadShopImage(configFile):
    idx = 1
    with open(configFile,"r") as f:
        for item in f:
            getPageImages(str(idx),item)
            idx+=1

runDownLoadShopImage("config.txt")
