#%%
from PyQt6.QtWidgets import QMainWindow
from untitled import Ui_MainWindow

class MW_Ext(Ui_MainWindow):
    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)#tham chiếu lớp cha Ui_MainWindow
        self.MainWindow = MainWindow
        #Connect events
        self.btnChon.clicked.connect(self.showContent)
    def showContent(self):
        self.lblContent.setText('Welcome to Fis')