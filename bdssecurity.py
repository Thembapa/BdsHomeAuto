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
        status_id=2
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

@app.route('/')
@app.route('/index')
def index():
   return  'Where do you think you are going?'

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="192.168.178.1", port=8080)
    app.run(host="192.168.8.128", port=9999)