#%%
#Nạp ứng dụng từ file.py được tạo ra từ file.ui
from PyQt6.QtWidgets import QApplication, QMainWindow
from untitled import Ui_MainWindow
from untitled_Extend import MW_Ext
import sys

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

w = QMainWindow()
f = Ui_MainWindow()
#f= MW_Ext()
f.setupUi(w)
w.show()
sys.exit(app.exec())