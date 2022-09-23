from twilio.rest import Client 
import bdsconfig
 
account_sid = bdsconfig.account_sid
auth_token = bdsconfig.auth_token
client = Client(account_sid, auth_token) 

#Make call
call = client.calls.create(
                        url='https://demo.twilio.com/welcome/voice/',
                        to='+27742280003',
                        from_='+18145593189'
                    )

print(call.sid)
 
#send msg 
#message = client.messages.create(  
#                              messaging_service_sid=bdsconfig.msg_serviceID, 
#                              body='Alerm triggered at house 145 Tembisa street',      
#                              to='+27782928514' 
#                          ) 
 
#print(message.sid)