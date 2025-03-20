from PyQt6.QtWidgets import QTabBar, QTableWidget, QTableWidgetItem, QMessageBox,QMainWindow
from grammar import Ui_MainWindow
from pymongo import MongoClient
from bson import ObjectId
#MongoDB Connection
client=MongoClient("mongodb://localhost:27017/")
db=client["exam_db"]
collection=db["grammar"]
class Grammar_content(QMainWindow,Ui_MainWindow):#Kế thừa lớp cha và giao diên
    def  __init__(self, topic_name,main_window):
        super().__init__()  # Khởi tạo QMainWindow
        self.setupUi(self)  # Gọi setup giao diện từ Ui_MainWindow
        self.topic_name = topic_name  # Lưu chủ đề đã chọn
        self.load_theory()  # Hiển thị nội dung của chủ đề
        self.pushButton_3.clicked.connect(self.back)
        self.main_window =main_window

    def load_theory(self):
        topic = collection.find_one({"type": self.topic_name})
        if topic:
        # Hiển thị chủ đề trong QLabel
            self.label_3.setText(topic["type"])
            content_text = ""
            for type_data in topic["types"]:
                content_text += f"📌 **{type_data['name']}**\n\n"
                # Nếu structure là chuỗi đơn giản
                if isinstance (type_data["structure"], str):
                    content_text += f"🔹 **Structure:** {type_data['structure']}\n\n"
                    # Nếu structure là object (có short_adj, long_adj)
                elif isinstance (type_data["structure"], dict):
                    for key, value in type_data["structure"].items():
                        content_text += f"🔹 **{key.replace('_', ' ').title()}**: {value}\n"
                    # Thêm Examples
                    content_text += "\n📖 **Examples:**\n"
                    for example in type_data["examples"]:
                        content_text += f"- {example}\n"

                    content_text += "\n" + "-" * 50 + "\n\n"  # Thêm khoảng cách giữa các types

                # Hiển thị nội dung trong QTextBrowser
                    self.textBrowser.setText(content_text)
                else:
                    self.label_3.setText("Không tìm thấy dữ liệu.")
    def back(self):
        self.main_window.show()  # Hiển thị lại cửa sổ chính
        self.close()




