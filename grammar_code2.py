from PyQt6.QtWidgets import QTabBar, QTableWidget, QTableWidgetItem, QMessageBox
from grammar import Ui_MainWindow
from pymongo import MongoClient
from bson import ObjectId
#MongoDB Connection
client=MongoClient("mongodb://localhost:27017/")
db=client["exam_db"]
collection=db["beers"]