# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint
from urlparse import urlparse
from flask import Flask

EMAIL = "Julia.r@yumasoft.com"
PASSWORD = "Jack01012000"

import urllib
import subprocess
import mechanize

def ttstamp_gen(fb_dtsg):
    u = ''
    for v in fb_dtsg:
        u += ord(v)
    return '2'+u

def add_cookie(name, value, domain, version=0, expires=365, port=None, port_specified=False, domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=True, discard=False, comment=None, comment_url=None, rest={'HttpOnly': False}, rfc2109=False):
    return mechanize.Cookie(version=version, name=name, value=value, expires=expires, port=port, port_specified=port_specified, domain=domain, domain_specified=domain_specified, domain_initial_dot=domain_initial_dot, path=path, path_specified=path_specified, secure=secure, discard=discard, comment=comment, comment_url=comment_url, rest=rest, rfc2109=rfc2109)

class CliCurl():

    def __init__(self, url):
        self.url = url
        self.cookie = None
        self.referer_link = urlparse(url).scheme + '://' + urlparse(url).netloc
        self.referer = None
        pass

    def add_cookie(self, cookiejar=[]):
        self.cookie_dict = {}
        cookie = self.cookie
        if not cookie:
            cookie = 'Cookie: '
        for c in cookiejar:
            cookie += c.name + '=' + c.value + '; '
            self.cookie_dict[c.name] = c.value
        self.cookie = cookie

    def add_referer(self, url=None):
        referer = 'Referer: '
        if not url:
            referer += self.referer_link
        else:
            referer += url
        self.referer = referer

    def compile(self):
        url = self.url
        if self.referer is None:
            self.add_referer()
        command = "curl '" + self.url + "'"
        headers = [
            'Host: www.facebook.com',
            'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: en-US,en;q=0.5',
            'Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
            self.cookie,
            self.referer
        ]
        for h in headers:
            command += " -H '" + h + "' "
        data = urllib.urlencode(self.data, True)
        data = urllib.unquote(data)
        print(data)
        command += " --data '" + data + "'"
        pprint(command)
        return command

    def run(self, data = {}):
        self.data = data
        pprint(data)
        proc = subprocess.Popen(self.compile(), shell=True, stdout=subprocess.PIPE )
        a = proc.communicate()
        pprint(a)
        return a




app = Flask(__name__)


@app.route('/')
def index():

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.FileCookieJar(filename="/home/igor/PycharmProjects/fb_parser/cookies.txt")

    browser.set_cookiejar(cookies)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US)     AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
    browser.open("https://login.facebook.com/login.php?login_attempt=1")
    browser.select_form(nr=0)

    browser.form['email'] = EMAIL
    browser.form['pass'] = PASSWORD
    browser.submit()
    data = {
        'ft_ent_identifier': '735272899920440',
        'comment_text': 'amazing',
        'source': '22',
        'client_id': '1429632677205%3A3425397009',
        'reply_fbid': '',
        'parent_comment_id': '',
        'rootid': 'u_ps_0_0_k',
        'clp': '',
        'attached_sticker_fbid': '0',
        'attached_photo_fbid': '0',
        'feed_context': '%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A308106089303792%2C%22outer_object_element_id%22%3A%22u_ps_0_0_0%22%2C%22object_element_id%22%3A%22u_ps_0_0_0%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D',
        'ft[tn]': '[]',
        'ft[fbfeed_location]': '36',
        'nctr[_mod]': 'pagelet_timeline_main_column',
        'av': '100009110845526',
        '__user': '100009110845526',
        '__a': '1',
        '__dyn': '', #пустой
        '__req': 'c',
        'fb_dtsg': 'AQEkxiOYhtrJ', # инпут в теле документа
        'ttstamp': '26581716611911872109105876676',
        '__rev': '1699252',
    }
    browser.add_password('https://www.facebook.com/', EMAIL, PASSWORD)
    b = browser.open('https://www.facebook.com/identity_switch.php', data='fb_dtsg=AQEtVwC7pYY-&url=https%3A%2F%2Fwww.facebook.com%2FSoftProposal&user_id=1411504542495570')
    # b = browser.open('https://www.facebook.com/softproposal')
    br = b.read().decode('utf-8')
    ret = br.find('"token":"AQ')
    c = CliCurl('https://www.facebook.com/ajax/ufi/add_comment.php')
    pprint(cookies)
    c.add_cookie(cookies)
    data['fb_dtsg']=br[ret+9:ret+21]
    # data['ttstamp'] = ttstamp_gen(data['fb_dtsg'])
    data['ft_ent_identifier'] = '119266071586184'
    from_user = c.cookie_dict['i_user'] if c.cookie_dict['i_user'] else c.cookie_dict['c_user']
    data['av'] = data['__user'] = from_user

    # c.run(data)
    return c.run(data)



if __name__ == '__main__':
    app.debug = True
    app.run()

data = {
    'ft_ent_identifier': '713648268749570',
    'comment_text': ')))',
    'source': '22',
    'client_id': '1429619899641%3A2374261221',
    'reply_fbid': '',
    'parent_comment_id': '',
    'rootid': 'u_ps_0_0_k',
    'clp': '',
    'attached_sticker_fbid': '0',
    'attached_photo_fbid': '0',
    'feed_context': '%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A308106089303792%2C%22outer_object_element_id%22%3A%22u_ps_0_0_0%22%2C%22object_element_id%22%3A%22u_ps_0_0_0%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D',
    'ft[tn]': '[]',
    'ft[fbfeed_location]': '36',
    'nctr[_mod]': 'pagelet_timeline_main_column',
    'av': '100009110845526',
    '__user': '100009110845526',
    '__a': '1',
    '__dyn': '7nmajEyl2lm9o-t2u5bGya4Au7qK78hACF3ozBDirWo8popyUWdwIhEngK5Uc-dwIxbxjUCi4EOGy9KbK',
    '__req': 'c',
    'fb_dtsg': 'AQGBwvHmiWBL',
    'ttstamp': '26581716611911872109105876676',
    '__rev': '1699252',
}
"""
https://www.facebook.com/ajax/ufi/add_comment.php?=&=&__a=1&__dyn=7nmajEyl2lm9o-t2u5bGya4Au7qK78hACF3ozBDirWo8popyUWdwIhEngK5Uc-dwIxbxjUCi4EOGy9KbK&__req=k&__rev=1699252&__user=100009110845526&attached_photo_fbid=0&attached_sticker_fbid=0&av=100009110845526&client_id=1429624469744%3A3305884792&clp=&comment_text=test&fb_dtsg=AQGWRsburWC6&feed_context=%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A308106089303792%2C%22outer_object_element_id%22%3A%22u_ps_0_0_0%22%2C%22object_element_id%22%3A%22u_ps_0_0_0%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D&ft%5Bfbfeed_location%5D=36&ft%5Btn%5D=%5B%5D&ft_ent_identifier=735272899920440&nctr%5B_mod%5D=pagelet_timeline_main_column&parent_comment_id=&reply_fbid=&rootid=u_ps_0_0_k&source=22&ttstamp=2658171878211598117114876754
"""

# sock = f.send_request('https://www.facebook.com/ajax/ufi/add_comment.php', '?=&=&__a=1&__dyn=7nmajEyl2lm9o-t2u5bGya4Au7qK78hACF3ozBDirWo8popyUWdwIhEngK5Uc-dwIxbxjUCi4EOGy9KbK&__req=k&__rev=1699252&__user=100009110845526&attached_photo_fbid=0&attached_sticker_fbid=0&av=100009110845526&client_id=1429624469744%3A3305884792&clp=&comment_text=test&fb_dtsg=AQGWRsburWC6&feed_context=%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A308106089303792%2C%22outer_object_element_id%22%3A%22u_ps_0_0_0%22%2C%22object_element_id%22%3A%22u_ps_0_0_0%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D&ft%5Bfbfeed_location%5D=36&ft%5Btn%5D=%5B%5D&ft_ent_identifier=735272899920440&nctr%5B_mod%5D=pagelet_timeline_main_column&parent_comment_id=&reply_fbid=&rootid=u_ps_0_0_k&source=22&ttstamp=2658171878211598117114876754')
# sock = f.open('http://www.facebook.com/softproposal')
# pprint(sock.read().decode('koi-7'))
# pprint(f.login2())
