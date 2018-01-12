#conding:UTF-8
#!usr/bin/python3
import requests
import re
import bs4
import traceback
urltemplate = "https://%s.fang.lianjia.com/loupan/"
log = open("error2.txt",'w',encoding = "UTF-8")
result = open("alldata2.txt",'w',encoding = "utf-8")
def sparsePage(page,city,pagenum):
    soup = bs4.BeautifulSoup(page.text)
    div = soup.find(name = "div",attrs = {"class":"house-lst"})
    ul = div.find(name="ul")
    hs = ul.find_all(name="div",attrs={"class":"col-1"})###获取第一列数据
    ps = ul.find_all(name="div",attrs={"class":"col-2"})
    if hs != None and ps != None:
        try:
            for i in range(len(hs)):
                h = hs[i]
                name ="";region = "";htype = "";area = "";jushi = "";mianji = "";price = "" ###开始进行解析
                name = h.a.text
                rows = h.find_all(name = "div",attrs = {"class":"row"})
                assert (len(rows)==2)
                region = rows[0].find(name = "a",attrs = {"class":"region"}).text
                htype = h.find(name ="span",attrs = {"class":"propertype label"}).text
                area = rows[1].find(name = "a",attrs={"class":"area"}).text
                if len(area.split('-'))==2:
                    jushi = area.split(' ')[0].strip()
                    mianji = area.split(' ')[1].strip()
                else:
                    pass
                p = ps[i]
                divpri = p.find(name = "div",attrs = {"class":"average"})
                if price !=None:
                    price = divpri.text.strip()
                result.write(city+"$"+name+"$"+region+"$"+price+"$"+htype+"$"+jushi+"$"+mianji+"&\n")
        except AttributeError as e:
            if name != "":
                log.write(city+str(pagenum)+name+":\n")
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
            print("getpage error")
            break
        if page.status_code ==200:
            pass
        else:
            print ("geterror")
            log.write("can't get page:",url)
            break
        page.encoding = "utf-8"
        sparsePage(page,city,pagenum)
        soup = bs4.BeautifulSoup(page.text)
        dd=soup.body.find(name = "div", attrs ={"class":"pagination"})
        tx = dd.attrs['data-totalpage']
        totalpages = int(tx)
        pagenum = pagenum+1
        if not (pagenum > totalpages):
            url = urltemplate %city +"pg"+str(pagenum)+"/"
        else:
            url =None
    print (city,"    ",pagenum)

if __name__ == "__main__":
    cities = ['su','sh']##
    Chinesename=['苏州','上海']
    for city in cities:
        handlecity(city)
    result.close()
    log.close()
