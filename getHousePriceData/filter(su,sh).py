#conding:utf-8
#!usr/bin/python3
import re
import sqlite3
cities = ['su','sh']##
Chinesename=['苏州','上海']
def processdata(file,cur):
	text = file.read()
	datalist  = text.split("&")
	for data in datalist:
		if data == '':
			pass
		else:
			try:
				attris = data.split("$")
				assert(len(attris)==7)
				rcity  = attris[0];rdistrict = attris[2];rname = attris[1];rprice = attris[3];rhuxing = attris[4];rmianji = attris[6];rjushi =attris[5]
				if rcity == '':
					print("the city is Null")
				else:
					rcity = rcity.strip()
					for i in range(len(cities)):
						if cities[i] == rcity:
							city = Chinesename[i]
				data_dis = re.split("[【|】]",rdistrict)
				if len(data_dis)!=3:
					print (rdistrict)
					print ("!!!!!!")
					district = None
				else:
					district = data_dis[1].split(" ")[0]
				if rname !='':
					name = rname
				else:
					print (data)
				if rjushi !='':
					jushi = rjushi
				else :
					jushi = None
				if rmianji =='':
					mianji = None
				else:
					mianji = re.sub("\D+[^~]?\D+",'',rmianji)
				price,label = handleprice(rprice)
				if label ==0:
					pass
				else:
					price = price *10000
					if mianji !=None:
						total =0
						digits = mianji.split("~")
						for digi in digits:
							total += int(digi)
						average = total/len(digits)*1.0
						price = price/(average*1.0)
					else:
						price = None
				if rhuxing !='':
					huxing = rhuxing
				else:
					huxing = None
				if city!=None and district!= None and name !=None:
					final = tuple([city,district,name,price,huxing,mianji,jushi])
					try:
						todatabase(cur,final)
					except sqlite3.IntegrityError:
						pass
				else:
					print (city,district,name)
			except AssertionError:
				pass


	
def handleprice(rprice):
	if re.search("元/m²",rprice)!=None:
		price = int(re.sub("\D+",'',rprice))
		lable = 0
		return price,lable
	elif re.search("万/套",rprice)!=None:
		price = int(re.sub("\D+",'',rprice))
		lable = 1
	else :
		price = None
		lable = 0
	return price,lable

def todatabase(cur,datalist):
    cur.execute('''insert into HousePrice
    				values(?,?,?,?,?,?,?)''',datalist)
if __name__ == "__main__":
	file = open("alldata2.txt",'r',encoding = 'utf-8')
	conn = sqlite3.connect("HousePrice(Chinesename).db")
	cur = conn.cursor()
	processdata(file,cur)
	cur.close()
	conn.commit()
	conn.close()



	

