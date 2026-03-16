import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đảm bảo bạn đã export file rsa.ui thành rsa.py trong thư mục ui
from ui.rsa import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- KẾT NỐI SỰ KIỆN (SIGNAL & SLOT) ---
        # Thiết lập các kết nối từ nút bấm trên giao diện tới các hàm xử lý API
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    # 1. HÀM TẠO KHÓA (GENERATE KEYS)
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.show_message("Thông báo", data["message"])
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # 2. HÀM MÃ HÓA (ENCRYPT)
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị kết quả mã hóa (dạng Hex) vào ô CipherText
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                self.show_message("Thành công", "Đã mã hóa dữ liệu thành công!")
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # 3. HÀM GIẢI MÃ (DECRYPT)
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Trả lại văn bản gốc vào ô Plain Text
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                self.show_message("Thành công", "Đã giải mã dữ liệu thành công!")
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # 4. HÀM KÝ SỐ (SIGN)
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị chữ ký vào ô Signature
                self.ui.txt_sign.setText(data["signature"])
                self.show_message("Thành công", "Đã tạo chữ ký số thành công!")
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # 5. HÀM XÁC THỰC (VERIFY)
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    self.show_message("Xác thực", "Chữ ký HỢP LỆ!")
                else:
                    self.show_message("Xác thực", "Chữ ký KHÔNG hợp lệ!", icon=QMessageBox.Warning)
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # Hàm bổ trợ hiển thị thông báo
    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    # Đảm bảo bạn đứng ở thư mục lab-03 khi chạy lệnh này
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())