import os
import sys
import json
import curl
import pycurl
import urllib
import cStringIO

from subprocess import Popen, PIPE

class createRequest():
    def __init__(self):
        self.user_id = self.git_config_get('user.name')
        self.pwd = self.git_config_get('user.password')

        if self.user_id == None or self.pwd == None:    
            print "Error getting username or password"
            return

        self.token = None
        self.write_buf = cStringIO.StringIO()
    
    def git_config_get(self, key):
        pipe = Popen(['git', 'config', '--get', key], stdout=PIPE)
        return pipe.communicate()[0].strip()

    def curl_cmd(self, url, post_params=None):     
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.USERPWD, "%s:%s" %(self.user_id, self.pwd))
        c.setopt(c.WRITEFUNCTION, self.write_buf.write)

        if post_params != None:
            c.setopt(pycurl.POSTFIELDS, post_params)

        c.perform()
        buf = self.write_buf.getvalue()
        http_code = c.getinfo(pycurl.HTTP_CODE)

        if http_code != 200 and http_code != 201:
            print "Error in getting the authentication token. %s" %(buf)
            return None

        self.write_buf.close()
        return buf
            
    def get_auth_token(self):
        auth_url = "https://api.github.com/authorizations" 
        params = "{\"scopes\":[\"repo\"]}"
        data = self.curl_cmd(auth_url, params)
        if data == None:    return 
            
        self.token = json.loads(data)['token'] 

    
    def get_top_users_by(self, number_users):
       print "generate_toke function"


if __name__ == '__main__':
    obj = createRequest()
    obj.get_auth_token()
