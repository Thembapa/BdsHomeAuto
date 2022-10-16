import json
import os
from flask import Flask, render_template, session, redirect, request, send_from_directory, url_for
import bdsconfig
import requests

#Application variables 
app = Flask(__name__, static_url_path='')
app.secret_key = "bdsHomeAuto"
 
def is_SignedIn():
    if 'ActiveUser' in session:
        return True
    else: 
        return False


@app.route('/deactivate_alert', methods=['GET', 'POST'])
@app.route('/deactivate_alert/<alert_id>')
def deactivate_alert(alert_id= None):
    status_id=1
    user_id=1
    zone=''
    if alert_id is not None:
        session['alert_id'] = alert_id
    if is_SignedIn():
        return redirect('/')
        if 'alert_id' in session:
            #Get alert status and details 
            param={'AlertID':session['alert_id']}
            url='https://api.bdstech.co.za/alert_status'
            alert_status = requests.get(url, json=param).json()
            zone =alert_status.get('Zone')
            print(alert_status)

    if request.method == 'POST':
        if status_id==1:
            session['ActiveUser'] = user_id
            return redirect('/deactivate_alert')
        elif status_id==2:
            if str(alert_status.get('OTP'))!='':
                user_otp = request.form["txt_OTP"]
                print('user_otp: ', user_otp,' server: ', alert_status.get('OTP'))
                if str(user_otp) == str(alert_status.get('OTP')):
                    print('Deactivated!')
                    url_diactivaete='https://api.bdstech.co.za/alert_deactivate'
                    resp_deacitvate = requests.get(url_diactivaete, json={'AlertID':session['alert_id'],'UserID' :user_id}).json()
                    print(resp_deacitvate)                
                    session.clear()
                    status_id=1
                    user_id=1
                    zone=''          
    
    return render_template('deactivate.html', status_id =status_id,zone=zone)

@app.route('/login', methods=['GET', 'POST'])
def login(alert_id= None):
    status_id=1
    user_id=1
    zone=''
    if alert_id is not None:
        session['alert_id'] = alert_id
    if is_SignedIn():
        status_id=2
        if 'alert_id' in session:
            #Get alert status and details 
            param={'AlertID':session['alert_id']}
            url='https://api.bdstech.co.za/alert_status'
            alert_status = requests.get(url, json=param).json()
            zone =alert_status.get('Zone')
            print(alert_status)

    if request.method == 'POST':
       print('Post command!')          
    
    return render_template('login.html', status_id =status_id,zone=zone)


@app.route('/sites')
def sites():
   #return  redirect('/login')
   Sites={'1':'WINDMILL PARK ESTATE','2':'VILLA LIZA PRIMARY SCHOOL','3':'THOMBO HOSPITAL'}
   


   return render_template('sites.html',Sites= Sites)

@app.route('/grantacc/<location_id>',methods=['GET', 'POST'])
@app.route('/grantacc/<location_id>/<AccessType>',methods=['GET', 'POST'])
def grantacc(location_id= None,AccessType=None):
   #return  redirect('/login')
   SiteName =''
   scanValues=[]
   Sites={'1':'WINDMILL PARK ESTATE','2':'VILLA LIZA PRIMARY SCHOOL','3':'THOMBO HOSPITAL'}
   SiteName=Sites[location_id]
   if request.method == 'POST':
    Scan =request.form["textBacode"]#'%MVL1CC64%0161%4025T053%1%40250135ZBZW%STZ031GP%FZG642S%Sedan (closed top) / Sedan (toe-kap) %CHEVROLET%AVEO%Red / Rooi%KL1TJ52Y66B497649%F15S3100839K%2021-11-30%'
    scanValues = Scan.split('%')
    print('len',len(scanValues),' ',scanValues)

   return render_template('access_control.html',SiteName= SiteName,location_id=location_id,scanValues= scanValues,AccessType= AccessType)

@app.route('/')
@app.route('/index')
def index():
    if not is_SignedIn():
        return redirect('/login')
   #return  redirect('/login')
    Task={'GRANT ACCESS':{'Url':'/sites','icon':'/images/icons/Access.png'}
                        ,'CHECK ALERTS':{'Url':'#','icon':'/images/icons/alert.png'}
                        ,'ACOUNT':{'Url':'#','icon':'/images/icons/account.png'}
                        ,'BILLING':{'Url':'#','icon':'/images/icons/bill.png'}
                        ,'TICKETS':{'Url':'#','icon':'/images/icons/ticket.png'}}

    return render_template('index.html',Task= Task)

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="192.168.178.1", port=8080)
    app.run(host="192.168.8.5", port=9999)