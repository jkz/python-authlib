import unittest

from authlib import oauth


class TestOAuth(unittest.TestCase):
    def test_signing(self):
        class App(oauth.App):
            key = 'xvz1evFS4wEEPTGEFPHBog'
            secret = 'kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw'

        class Token(oauth.Token):
            access_token = '370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb'
            access_token_secret = 'LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE'

        auth = oauth.Auth(App(), Token())

        method = 'POST'
        base_url = 'https://api.twitter.com/1/statuses/update.json'
        params_dict = dict(
            status = 'Hello Ladies + Gentlemen, a signed OAuth request!',
            include_entities = 'true',
        )
        header_dict = dict(
            oauth_app_key = auth.app.key,
            oauth_nonce = 'kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg',
            oauth_signature_method = 'HMAC-SHA1',
            oauth_timestamp = '1318622958',
            oauth_token = auth.token.access_token,
            oauth_version = '1.0',
        )

        combo_dict = {}
        combo_dict.update(params_dict)
        combo_dict.update(header_dict)
        computed_param_string = oauth.utils.encode_params(combo_dict)

        expected_param_string = "include_entities=true&oauth_app_key=xvz1evFS4wEEPTGEFPHBog&oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20signed%20OAuth%20request%21"
        self.assertEqual(expected_param_string, computed_param_string)

        expected_base_string = "POST&https%3A%2F%2Fapi.twitter.com%2F1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_app_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521"
        computed_base_string = oauth.utils.base_string(method, base_url, computed_param_string)
        self.assertEqual(expected_base_string, computed_base_string)

        expected_signing_key = "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
        computed_signing_key = auth.signing_key
        self.assertEqual(expected_signing_key, computed_signing_key)


        expected_signature = 'tnnArxj06cWHq44gCs1OSKk/jLY='
        computed_signature = auth.build_signature(computed_base_string)
        self.assertEqual(expected_signature, computed_signature)

    def test_authorize(self):
        '''
        app = Consumer()
        app.key = 'XxpEUc4jtBdSlUOeOYOoA'
        app.secret = 'DqapzgIyQ5S1CYpo2jblGo3ZWO38TlLYlagmGJAX3s'
        app.host = 'api.twitter.com'
        app.secure = True
        app.request_token_uri = 'https://api.twitter.com/oauth/request_token'
        #auth.token = token

        print ''
        print 40*'='
        print 'example'
        app.get_request_token()
        return
        '''

        class API(oauth.API):
            host = 'term.ie'
            request_token_path = '/oauth/example/request_token.php'

        class App(oauth.App):
            key = 'key'
            secret = 'secret'

        app = App()

        print 5 * '\n'
        print 40 * '='
        print 'term.ie'
        print API(app).get_request_token()
        return


        '''
        class GoogleAuth(Auth):
            host = 'google.com'
            secure = False
            request_token_uri = ''
        google = _uAuth(app)

        app = Consumer()
        app.key = 'XxpEUc4jtBdSlUOeOYOoA'
        app.secret = 'DqapzgIyQ5S1CYpo2jblGo3ZWO38TlLYlagmGJAX3s'

        twitter = Auth(app)
        twitter.host = 'api.twitter.com'
        twitter.secure = True
        twitter.get_request_token_uri = '/oauth/request_token'

        print 3 * '\n'
        print 40 * '='
        print 'twitter'
        twitter.get_request_token(oauth_callback='http://jessethegame.net/callback')
        return


        #callm = api.url.POST.oauth.example.request_token('.php')
        callm = auth.suspend.POST.oauth.example.request_token('.php')
        #callm = api(method='POST', mode='suspend')('/oauth/example/request_token.php')

        print str(callm)
        r = callm()
        print r.headers
        print r.raw
        token = Token()
        token.key = 'dummy_token_key'
        token.secret = 'dummy_token_secret'
        '''
