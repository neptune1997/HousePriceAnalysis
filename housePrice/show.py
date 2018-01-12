from flask import Flask, render_template, g, session 
from flask import request  
from flask import Response  
  
import json  
import sqlite3
import os
  
app = Flask(__name__) 
app.secret_key=os.urandom(20)

DATABASE = 'HousePrice.db' 
  
def Response_headers(content):  
    resp = Response(content)  
    resp.headers['Access-Control-Allow-Origin'] = '*'  
    return resp  
 
def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.route('/')  
def findCity():  
    return render_template("index.html")  
 
@app.route('/city/<cityName>')  
def getData(cityName):  
    session["cityName"]=cityName
    return render_template("show.html")
@app.route('/deal')  
def dealData():
    cityName = session.get('cityName')
    str=[{"cityName":cityName}]
    st={}
    cur=g.db.cursor()	
    result=cur.execute("SELECT district,avg(price) FROM HousePrice where city = ? group by district",(cityName,))
    for row in result:
        if row[1] is None:
            continue
        st={"district":row[0],"price":round(row[1],2)}
        str.append(st)
    datas = {  
        "data":str
    }  
    g.db.close()
    session.pop('cityName',None)
    content = json.dumps(datas)
    resp = Response_headers(content) 
    return resp  

@app.errorhandler(403)  
def page_not_found(error):  
    content = json.dumps({"error_code": "403"})  
    resp = Response_headers(content)  
    return resp  
 
@app.errorhandler(404)  
def page_not_found(error):  
    content = json.dumps({"error_code": "404"})  
    resp = Response_headers(content)  
    return resp  
 
@app.errorhandler(400)  
def page_not_found(error):  
    content = json.dumps({"error_code": "400"})  
    resp = Response_headers(content)  
    return resp  
 
@app.errorhandler(410)  
def page_not_found(error):  
    content = json.dumps({"error_code": "410"})  
    resp = Response_headers(content)  
    return resp  
 
@app.errorhandler(500)  
def page_not_found(error):  
    content = json.dumps({"error_code": "500"})  
    resp = Response_headers(content)  
    return resp 
	
if __name__ == '__main__':  
    app.run(debug=True) 