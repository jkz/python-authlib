class Provider(callm.Connection):
    host = 'example.com'

    AUTH_URL = 'https://www.facebook.com/dialog/oauth/'
    EXCHANGE_CODE_URL

provider = Provider()

service = Service(provider)

service.request_code('http://example.com/callback/')


