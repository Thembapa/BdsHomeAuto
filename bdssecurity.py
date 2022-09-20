from twilio.rest import Client 
import bdsconfig
 
account_sid = bdsconfig.account_sid
auth_token = bdsconfig.auth_token
client = Client(account_sid, auth_token) 
 
message = client.messages.create(  
                              messaging_service_sid=bdsconfig.msg_serviceID, 
                              body='This is a test xoxo',      
                              to='+27738195149' 
                          ) 
 
print(message.sid)