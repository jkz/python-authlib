import facebook
import oauth2

api = facebook.GraphAPI()

client = oauth2.OAuth2Client()
client.client_id = 'Hahathiswasmyrealid'
client.secret = 'andthismysecret'

token = oauth2.OAuth2Token()
token.access_token = "gladIdisabledthatbynow"

owner = oauth2.OAuth2ResourceOwner()
owner.client = client

api.auth = owner

url, state = api.request_code('dummy.com')
print str(url)

#print api.GET.me(mode='url')
#print api.GET.me()
