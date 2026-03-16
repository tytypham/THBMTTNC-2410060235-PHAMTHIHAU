import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect buttons
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt)
        self.ui.btn_decrypt.clicked.connect(self.decrypt)
        self.ui.btn_sign.clicked.connect(self.sign)
        self.ui.btn_verify.clicked.connect(self.verify)

    # Generate RSA keys
    def generate_keys(self):

        try:
            r = requests.get("http://127.0.0.1:5001/api/rsa/generate_keys")

            data = r.json()

            self.ui.txt_info.setText(data["message"])

            QMessageBox.information(self, "Success", data["message"])

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))

    # Encrypt
    def encrypt(self):

        message = self.ui.txt_plain_text.toPlainText()

        try:

            r = requests.post(
                "http://127.0.0.1:5001/api/rsa/encrypt",
                json={
                    "message": message,
                    "key_type": "public"
                }
            )

            data = r.json()

            self.ui.txt_cipher_text.setText(data["encrypted_message"])

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))

    # Decrypt
    def decrypt(self):

        cipher = self.ui.txt_cipher_text.toPlainText()

        try:

            r = requests.post(
                "http://127.0.0.1:5001/api/rsa/decrypt",
                json={
                    "ciphertext": cipher,
                    "key_type": "private"
                }
            )

            data = r.json()

            self.ui.txt_plain_text.setText(data["decrypted_message"])

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))

    # Sign
    def sign(self):

        message = self.ui.txt_plain_text.toPlainText()

        try:

            r = requests.post(
                "http://127.0.0.1:5001/api/rsa/sign",
                json={
                    "message": message
                }
            )

            data = r.json()

            self.ui.txt_sign.setText(data["signature"])

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))

    # Verify
    def verify(self):

        message = self.ui.txt_plain_text.toPlainText()
        signature = self.ui.txt_sign.toPlainText()

        try:

            r = requests.post(
                "http://127.0.0.1:5001/api/rsa/verify",
                json={
                    "message": message,
                    "signature": signature
                }
            )

            data = r.json()

            if data["is_verified"]:
                QMessageBox.information(self, "Verify", "Signature VALID")
            else:
                QMessageBox.warning(self, "Verify", "Signature INVALID")

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())