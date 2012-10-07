import facebook
import oauth2

api = facebook.GraphAPI()

client = oauth2.OAuth2Client()
client.client_id = '299095383509760'
client.secret = '5348ed456e34020d89a8abf6f76b51b0'

token = oauth2.OAuth2Token()
token.access_token = "AAACEdEose0cBALTXLuPIWT8ZCvCX0EWfbLj4mq2wOS29xGmu20ZAZCOjyN7d07xiBTeOQ2S46Jhd8Fw3xdd1ZAoyiItD4QxCGuckwMGVKZBDslflieyjS"

owner = oauth2.OAuth2ResourceOwner()
owner.client = client

api.auth = owner

url, state = api.request_code('dummy.com')
print str(url)

#print api.GET.me(mode='url')
#print api.GET.me()
