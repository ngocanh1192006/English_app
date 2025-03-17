import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication


#ensure Qapplication is created one
#app = Qapplication ([])
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

form, window = uic.loadUiType("login.ui")
w = window()
f = form()
f.setupUi(w)

w.show()

sys.exit(app.exec())