import json
import requests

def send_email(**kwargs):
    sender = kwargs.get('sender')
    to = kwargs.get('to')
    subject = kwargs.get('subject')
    html = kwargs.get('html')

    print(requests.post(
        'https://api.mailgun.net/v3/ronen.io/messages',
        auth=('api', 'key-dbbb9a77691f659f653d1bdb453dc265'),
        data={'from': sender,
          'to': to,
          'subject': subject,
          'html': html}))

    print('Sent email')

class EndpointsMixin(object):
    def get_prices(self, **params):
        endpoint  = 'v1/prices'
        return self.request(endpoint, params=params)

    def get_orders(self, account_id, **params):
        endpoint = 'v1/accounts/%s/orders' % (account_id)
        return self.request(endpoint, params=params)

    def create_order(self, account_id, **params):
        endpoint = 'v1/accounts/%s/orders' % (account_id)
        return self.request(endpoint, 'POST', params=params)

    def get_order(self, account_id, order_id, **params):
        endpoint = 'v1/accounts/%s/orders/%s' % (account_id, order_id)
        return self.request(endpoint, params=params)

    def modify_order(self, account_id, order_id, **params):
        endpoint = 'v1/accounts/%s/orders/%s' % (account_id, order_id)
        return self.request(endpoint, 'PATCH', params=params)

    def close_order(self, account_id, order_id, **params):
        endpoint = 'v1/accounts/%s/orders/%s' % (account_id, order_id)
        return self.request(endpoint, 'DELETE', params=params)

    def get_positions(self, account_id, **params):
        endpoint = 'v1/accounts/%s/positions' % (account_id)
        return self.request(endpoint, params=params)

    def get_position(self, account_id, instrument, **params):
        endpoint = 'v1/accounts/%s/positions/%s' % (account_id, instrument)
        return self.request(endpoint, params=params)

    def close_position(self, account_id, instrument, **params):
        endpoint = 'v1/accounts/%s/positions/%s' % (account_id, instrument)
        return self.request(endpoint, 'DELETE', params=params)


class API(EndpointsMixin, object):
    def __init__(self, environment='practice', access_token=None, headers=None):   
        if environment == 'sandbox':
            self.api_url = 'http://api-sandbox.oanda.com'
        elif environment == 'practice':
            self.api_url = 'https://api-fxpractice.oanda.com'
        elif environment == 'live':
            self.api_url = 'https://api-fxtrade.oanda.com'

        self.access_token = access_token
        self.client = requests.Session()

        if self.access_token:
            self.client.headers['Authorization'] = 'Bearer ' + self.access_token

        if headers:
            self.client.headers.update(headers)

    def request(self, endpoint, method='GET', params=None):
        url = '%s/%s' % (self.api_url, endpoint)

        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)

        request_args = {}
        if method == 'get':
            request_args['params'] = params
        else:
            request_args['data'] = params

        try:
            response = func(url, **request_args)
            content = response.content.decode('utf-8')
            content = json.loads(content)
        except requests.RequestException as e:
            print('API Error')
            print(e)
        except:
            print('Warning Exception')
            time.sleep(5)
            response = func(url, **request_args)
            content = response.content.decode('utf-8')
            content = json.loads(content)
            message = 'Warning Exception while interacting with api url: {}'.format(url)
            send_email(sender='intelligence@ronen.io', to='ronensinger17@gmail.com', subject='Grid S_1 Fucked', html='<pre>'+message+'</pre>')

        if response.status_code >= 400:
            raise OandaError(content)

        return content

class OandaError(Exception):
    def __init__(self, error_response):
        msg = 'OANDA API returned error code %s (%s) ' % (error_response['code'], error_response['message'])

        super(OandaError, self).__init__(msg)