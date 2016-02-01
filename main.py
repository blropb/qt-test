import sys
from PyQt5.QtWidgets import QApplication
from browser import Browser


app = QApplication(sys.argv)
b = Browser(app)
b.test()

sys.exit(app.exec_())