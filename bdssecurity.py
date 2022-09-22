from twilio.rest import Client 
import bdsconfig
 
account_sid = bdsconfig.account_sid
auth_token = bdsconfig.auth_token
client = Client(account_sid, auth_token) 

#Make call
call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+27742280003',
                        from_='+27738195149'
                    )

print(call.sid)
 
#send msg 
#message = client.messages.create(  
#                              messaging_service_sid=bdsconfig.msg_serviceID, 
#                              body='Alerm triggered at house 145 Tembisa street',      
#                              to='+27782928514' 
#                          ) 
 
#print(message.sid)