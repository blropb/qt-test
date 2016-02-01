__author__ = 'igor'
import sys
import config
from pprint import pprint
from PyQt5.QtCore import QEventLoop, QUrl, QCoreApplication, QObject, QByteArray, pyqtSignal, QVariant, QPoint, pyqtSlot, QTimer, QThread
from PyQt5.QtGui import QGuiApplication
from PyQt5 import QtWebKit, QtWidgets
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QNetworkCookieJar
from PyQt5.QtWebKitWidgets import QWebView, QWebPage, QWebFrame
from PyQt5.QtWidgets import QApplication
from webview import WebView
import  random  as  random_number

class Browser(QObject):

    comment_postdata_example = {
            'ft_ent_identifier': '735272899920440', # ИД сообщения
            'comment_text': 'Cool))', # Текст коментария
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
            'ft[top_level_post_id]': '750869418360788',
            'ft[fbfeed_location]': '36',
            'nctr[_mod]': 'pagelet_timeline_main_column',
            'av': '100009110845526',
            '__user': '100009110845526',
            '__a': '1',
            '__dyn': '', #пустой
            '__req': 'c',
            'fb_dtsg': 'AQEkxiOYhtrJ', # инпут в теле документа
            'ttstamp': '26581716611911872109105876676',
            '__rev': '1713404',
        }

    def __init__(self, parent):
        super().__init__(parent)
        self.set_url('http://google.ru')
        conn = QNetworkAccessManager()
        self.conn = conn
        self.r = QNetworkRequest()
        self.r.attribute(QNetworkRequest.CookieSaveControlAttribute, QVariant(True))
        # self.r.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
        # self.r.setRawHeader("Referer", "http://www.facebook.com/")
        # self.r.setRawHeader("Host", "www.facebook.com")
        self.cj = QNetworkCookieJar()
        conn.setCookieJar(self.cj)
        conn.createRequest = self._create_request
        self.wv = WebView()
        self.wv.show()
        self.wv.page().setNetworkAccessManager(conn)
        # self.wv.auth()
        self.loop = QEventLoop()
        pass

    def _create_request(self, operation, request, data):
        # print(data)
        reply = QNetworkAccessManager.createRequest(self.conn,
                                                    operation,
                                                    request,
                                                    data)
        self.conn.new_reply = reply
        self.wv_reply = reply
        return reply

    def set_url(self, url):
        if isinstance(url, QByteArray):
            self.url = QUrl().fromEncoded(url)
        else:
            self.url = QUrl(url)

    def send_request(self, post=None, data={}):
        loop = QEventLoop()
        self.r.setUrl(self.url)
        if post:
            encoded_data = self._urlencode_post_data(data)
            pprint(encoded_data)
            self.reply_post = self.conn.post(self.r, encoded_data)
            self.reply_post.downloadProgress.connect(self.prepare_responce)

        else:
            self.reply = self.conn.get(self.r)
            self.reply.finished.connect(self.prepare_responce)
        # return \
        loop.exec()

    def prepare_responce(self):
        # self.check_redirect()
        self.responce = self.reply_post.readAll()#.data().decode('utf-8')
        pprint(self.responce)
        sys.exit()

    def check_redirect(self):
        print(self.url)
        a = self.reply.rawHeader('Location')

        if len(a) > 0:
            self.set_url(a)
            self.send_request()
        else:
            self.loop.exit()

    def test(self):
        self.wv.auth('https://www.facebook.com/freelanceuidesignerdeveloper')
        self.wv.authentication.connect(self.webview_login)

    def _urlencode_post_data(self, post_data):
        post_params = []
        for (key, value) in post_data.items():
            print(key, value)
            post_params.append(key+'='+value)
        return '&'.join(post_params)

    def webview_login(self):
        text_page = self.wv.page().mainFrame().toHtml()
        data = {
            'ft_ent_identifier': '735272899920440',
            'comment_text': 'amazing',
            'source': '22',
            'client_id': '1429632677205%3A3425397009',
            'reply_fbid': '',
            'parent_comment_id': '',
            'rootid': 'u_ps_0_0_o',
            'clp': '',
            'attached_sticker_fbid': '0',
            'attached_photo_fbid': '0',
            'feed_context': '%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A308106089303792%2C%22outer_object_element_id%22%3A%22u_ps_0_0_0%22%2C%22object_element_id%22%3A%22u_ps_0_0_0%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D',
            'ft[tn]': '[]',
            'ft[top_level_post_id]': '',
            'ft[fbfeed_location]': '36',
            'nctr[_mod]': 'pagelet_timeline_main_column',
            'av': '100009110845526',
            '__user': '100009110845526',
            '__a': '1',
            '__dyn': '', #пустой
            '__req': 'c',
            'fb_dtsg': 'AQEkxiOYhtrJ', # инпут в теле документа
            'ttstamp': '26581716611911872109105876676',
            '__rev': '1713404',
        }
        dtsg_index = text_page.find('"token":"AQ')
        data['fb_dtsg'] = text_page[dtsg_index+9:dtsg_index+21]
        data['ttstamp'] = self.ttstamp_gen(data['fb_dtsg'])
        data['ft_ent_identifier'] = '849713745045784' # self.get_post_id(post_object)
        data['comment_text'] = random_number.choice(config.comments_list)
        pprint(data['comment_text'])


        # data['av'] = data['__user'] = from_user
        # self.applyMetaData()
        self.url = QUrl('https://www.facebook.com/ajax/ufi/add_comment.php')
        self.send_request(True, data)
        sys.exit()


    def applyMetaData(self):
        print('applyMetaData')
        raw_header = {
            'Host': 'www.facebook.com',
            'User-Agent': ' Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
            'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': ' en-US,en;q=0.5',
            'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': ' https://www.facebook.com/SoftProposal?fref=nf',
        }
        for (key, header) in raw_header.items():
            self.r.setRawHeader(key, header)

    @staticmethod
    def ttstamp_gen(fb_dtsg):
        u = ''
        for v in fb_dtsg:
            u += str(ord(v))
        return '2'+u
    @staticmethod
    def get_post_id(post):
        if post.object_id:
            return post.object_id
        else:
            str = post.id.split('_')
            if len(str) > 1:
                return str[0]
            else:
                post.id

