__author__ = 'igor'
import config
from pprint import pprint
from PyQt5.QtCore import QEventLoop, QUrl, QCoreApplication, QObject, QByteArray, pyqtSignal, QVariant, QPoint, pyqtSlot, QTimer, QThread
from PyQt5.QtGui import QGuiApplication
from PyQt5 import QtWebKit, QtWidgets
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QNetworkCookieJar
from PyQt5.QtWebKitWidgets import QWebView, QWebPage, QWebFrame
from PyQt5.QtWidgets import QApplication
import  random  as  random_number


class WebView(QWebView):

    authentication = pyqtSignal()

    def __init__(self):
        QWebView.__init__(self)
        settings = self.settings()
        settings.setAttribute(settings.AutoLoadImages, False)

        self.authorize = False
        self.feed_list = []
        self.page_loaded = False
        self.scroll_down = False
        self.page_height = 0
        self.run_timer = True
        self.trg_func = self.cap
        self.textpage = None

        self.loadFinished.connect(self.set_textpage)
        # self.page().mainFrame().contentsSizeChanged.connect(self.scroll_down_trigger)

    @pyqtSlot()
    def set_textpage(self):
        self.textpage = self.page().mainFrame().toHtml()


    def get_random_login_pair(self):
        logins = list(config.logins_list.copy().keys())
        pprint(list(logins))
        login = random_number.choice(logins)
        return {'email': login, 'pass': config.logins_list[login]}

    @pyqtSlot()
    def scroll_down_trigger(self):
        # print('scroll down trigger')
        if self.scroll_down:
            if self.run_timer:
                self.test_timer = False
                QTimer.singleShot(5000, self.scroll_down_func)

    def scroll_down_func(self):
        y = self.page().mainFrame().contentsSize().height()
        self.page().mainFrame().setScrollBarValue(0, y)
        self.run_timer = True
        # print("scroll down func")
        if self.check_loading():
            self.trg_func()

    def login(self):
        print('Authorized')
        web = self
        login = self.get_random_login_pair()
        frame = web.page().mainFrame()
        document = frame.documentElement()
        email = document.findFirst("input[name=email]")
        email.setAttribute("value", login['email'])

        passw = document.findFirst("input[name=pass]")
        passw.setFocus()
        passw.setAttribute("value", login['pass'])
        button = document.findFirst("input[type=submit]")
        button.evaluateJavaScript("this.click()")
        print('end login')
        self.page_height = self.page().mainFrame().contentsSize().height()

    @pyqtSlot()
    def webview_trigger(self):
        if not self.has_auth():
            self.login()
        else:
            self.trg_func()

    def has_auth(self):
        if self.authorize:
            return True
        text_page = self.page().mainFrame().toHtml()
        # pprint(self.page().networkAccessManager().new_reply.rawHeaderList())
        if "Logout" in text_page:
            self.authorize = True
            self.authentication.emit()
            return True
        else:
            return False
        pass

    def check_loading(self):

        frame = self.page().mainFrame()
        document = frame.documentElement()
        feed = document.evaluateJavaScript("""
a = document.getElementsByClassName('uiMorePagerLoader pam uiBoxLightblue')
b = true
function isHidden(el) {
    return (el.offsetParent === null)
};
if(a.length > 0)
{
  isHidden(a[0]);
} else {
  b;
}""")
        # print('Check loading: ', feed)
        if feed == 'true':
            return True
        elif feed == 'false':
            return False
        else:
            return None

    def open(self, url):
        # self.trg_func = self.get_posts_from_page
        # self.scroll_down = True
        # self.scroll_down_trigger()
        self.load(QUrl(url))

    def auth(self, url='https://www.facebook.com'):
        self.open(url)
        self.loadFinished.connect(self.webview_trigger)


    def get_posts_from_page(self):
        if self.check_loading():
            return False
        frame = self.page().mainFrame()
        document = frame.documentElement()
        feed = document.evaluateJavaScript("""
a = document.getElementsByName('feedback_params')
ar = Array()
for (index = 0; index < a.length; ++index) {
    ar.push(a[index].value);
}
ar
        """)
        # print(feed)
        for p in feed:
            if p not in self.feed_list:
                self.feed_list.append(p)
        print(len(self.feed_list))

    def cap(self):
        pass
