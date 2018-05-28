from bitcoinrpc.authproxy import AuthServiceProxy,JSONRPCException
from pprint import pprint
import requests
import json


class connector(object):
    def __init__(self,name,password):
        self.name = name
        self.password = password

    def get_url_to_connect(self):
        return 'http://%s:%s@127.0.0.1:18332'%(self.name,self.password)

    def connect(self):
        url_to_connect = self.get_url_to_connect()
        print url_to_connect
        return AuthServiceProxy(url_to_connect)

    # if bitcoinrpc dont have a method,that you want to use,lets call this function
    def send_request_to_rpc_server(self,method,params = []):
        headers = {"content-type": "application/json"}
        url = self.get_url_to_connect();
        data = {
            "method": method,
            # params should be list
            "params": [params] if type(params)!= list else params
        }
        r = requests.post(url, headers= headers, data= json.dumps(data))
        return r.json()['result']
