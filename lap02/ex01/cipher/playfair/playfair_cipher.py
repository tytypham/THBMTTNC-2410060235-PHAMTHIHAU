class PlayFairCipher:
    def __init__(self):
        pass

    # Tạo ma trận 5x5
    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix_list = []

        # Thêm key trước (loại bỏ trùng)
        for char in key:
            if char not in matrix_list and char in alphabet:
                matrix_list.append(char)

        # Thêm các chữ còn lại
        for char in alphabet:
            if char not in matrix_list:
                matrix_list.append(char)

        # Chia thành ma trận 5x5
        matrix = [matrix_list[i:i+5] for i in range(0, 25, 5)]
        return matrix

    # Tìm tọa độ chữ cái
    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col

    # Mã hóa
    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I").upper()
        encrypted_text = ""

        # Nếu lẻ thì thêm X
        if len(plain_text) % 2 != 0:
            plain_text += "X"

        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:
                encrypted_text += (
                    matrix[row1][(col1 + 1) % 5] +
                    matrix[row2][(col2 + 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:
                encrypted_text += (
                    matrix[(row1 + 1) % 5][col1] +
                    matrix[(row2 + 1) % 5][col2]
                )

            # Hình chữ nhật
            else:
                encrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        return encrypted_text

    # Giải mã
    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            # Cùng hàng
            if row1 == row2:
                decrypted_text += (
                    matrix[row1][(col1 - 1) % 5] +
                    matrix[row2][(col2 - 1) % 5]
                )

            # Cùng cột
            elif col1 == col2:
                decrypted_text += (
                    matrix[(row1 - 1) % 5][col1] +
                    matrix[(row2 - 1) % 5][col2]
                )

            # Hình chữ nhật
            else:
                decrypted_text += (
                    matrix[row1][col2] +
                    matrix[row2][col1]
                )

        # Loại bỏ X dư nếu có
        if decrypted_text.endswith("X"):
            decrypted_text = decrypted_text[:-1]

        return decrypted_text