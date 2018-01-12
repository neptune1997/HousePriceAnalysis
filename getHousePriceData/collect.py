#coding:utf-8
#!usr/bin/python3
import requests
import re
import bs4
import traceback
urltemplate = "https://%s.fang.lianjia.com/loupan/"
log = open("error.txt",'w',encoding = "UTF-8")
result = open("alldata.txt",'w',encoding = "utf-8")

def sparsePage(page,city,pagenum):
    soup = bs4.BeautifulSoup(page.text)
    ul = soup.find(name="ul",attrs={"id":"house-lst"})
    hs = ul.find_all(name="div",attrs={"class":"col-1"})###获取第一列数据
    ps = ul.find_all(name="div",attrs={"class":"col-2"})
    if hs != None and ps != None:
        try:
            for i in range(len(hs)):
                h = hs[i]
                name ="";region = "";htype = "";area = "";jushi = "";mianji = "";price = "" ###开始进行解析
                name = h.a.text
                region = h.find(name = "span",attrs = {"class":"region"}).text
                htype = h.find(name ="span",attrs = {"class":"live"}).text
                area = h.find(name = "div",attrs={"class":"area"}).text
                if len(area.split('-'))==2:
                    jushi = area.split('-')[0].strip()
                    mianji = area.split('-')[1].strip()
                else:
                    pass
                p = ps[i]
                divpri = p.find(name = "div",attrs = {"class":"average"})
                if price !=None:
                    price = divpri.text.strip()
                result.write(city+"$"+name+"$"+region+"$"+price+"$"+htype+"$"+jushi+"$"+mianji+"&")
        except AttributeError as e:
            if name != "":
                log.write(city+pagenum+name+":\n")
            traceback.print_exc(file = log)
    else:
        log.write(city+str(pagenum)+":\n sparse page failed")
def handlecity(city):
    pagenum=1
    url = urltemplate %city
    while url != None:
        try:
            page = requests.get(url,verify = False)
        except:
            pass
        if page.status_code ==200:
            pass
        else:
            print ("geterror")
            log.write("can't get page:",url)
            break
        page.encoding = "utf-8"
        sparsePage(page,city,pagenum)
        soup = bs4.BeautifulSoup(page.text)
        dd=soup.body.find(name = "div", attrs ={"class":"page-box house-lst-page-box"})
        tx = dd.attrs['page-data']
        tx = tx.split(",")[0]
        digit=tx.split(":")[1]
        totalpages = int(digit)
        pagenum = pagenum+1
        if not (pagenum > totalpages):
            url = urltemplate %city +"pg"+str(pagenum)+"/"
        else:
            url =None
    print (city,"    ",pagenum)

if __name__ == "__main__":
    #page = requests.get("https://dl.fang.lianjia.com/loupan/pg2/")
    cities = ['dl','bj','cd','cq','cs','gz','hz','jn','nj','qd','sz','wh','xm','xa','zz','km','sy','hui','hf','ty']##
    Chinesename=['大连','北京','成都','重庆','长沙','广州','杭州','济南','南京','青岛','深圳','武汉','厦门','西安','郑州','昆明','沈阳','惠州','合肥','太原']
    for city in cities:
        handlecity(city)
    result.close()
    log.close()
