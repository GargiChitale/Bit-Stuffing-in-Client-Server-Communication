import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import sys

receiver_id = 211
sender_id = 211
flag = '01111110'

class ServerThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def bit_destuffing(self, data):
        destuffed_data = ""
        consecutive_ones = 0
        for bit in data:
            if bit == '1':
                consecutive_ones += 1
            else:
                consecutive_ones = 0

            destuffed_data += bit

            # Handle destuffing: if 5 consecutive '1's are followed by '0', skip the stuffed '0'
            if consecutive_ones == 5 and bit == '0':
                destuffed_data = destuffed_data[:-1]

        return destuffed_data

    def process_word(self, word):
        # Process the complete message (destuffing, removing header, etc.)
        destuffed_data = self.bit_destuffing(word)
        clean_data = destuffed_data[16:].replace(flag, '')

        # Emit the clean data for printing
        self.message_received.emit(f"Received data after removing flag and header: {clean_data}")

        # Convert binary data to ASCII
        ascii_text = self.binary_to_ascii(clean_data)
        self.message_received.emit(f"Received data as ASCII: {ascii_text}")

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 12346
        server.bind((host, port))
        server.listen(1)

        self.message_received.emit("Server is waiting for connection...")

        conn, addr = server.accept()
        self.message_received.emit(f"Connected to: {addr}")

        received_data = ""  # To store all the received words
        data_buffer = ""   # To accumulate partial data

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            self.message_received.emit(f"Received data from client: {data}")

            # Accumulate the data until the flag is detected
            data_buffer += data
            while flag in data_buffer:
                # Find the index of the flag
                flag_index = data_buffer.find(flag)

                # Extract the complete message up to the flag
                complete_message = data_buffer[:flag_index]

                # Process each word in the complete message
                words = complete_message.split(flag)
                for word in words:
                    if word:
                        self.process_word(word)

                # Remove the processed data from the buffer
                data_buffer = data_buffer[flag_index + len(flag):]

        conn.close()

    def binary_to_ascii(self, binary_data):
        # Split the binary data into 8-bit chunks
        binary_chunks = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

        # Convert each 8-bit chunk to decimal
        decimal_values = [int(chunk, 2) for chunk in binary_chunks]

        # Replace non-printable ASCII characters with '.'
        printable_characters = [chr(value) if 32 <= value <= 126 else '.' for value in decimal_values]

        # Join the characters to form the final ASCII text
        ascii_text = ''.join(printable_characters)

        return ascii_text

class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.server_output = QTextEdit()
        self.server_output.setReadOnly(True)
        self.layout.addWidget(self.server_output)

        self.central_widget.setLayout(self.layout)

        self.server_thread = ServerThread()
        self.server_thread.message_received.connect(self.update_server_output)
        self.server_thread.start()

    def update_server_output(self, message):
        self.server_output.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server_window = ServerWindow()
    server_window.show()
    sys.exit(app.exec_())

