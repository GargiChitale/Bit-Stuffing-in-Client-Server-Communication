import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys

receiver_id = 211
sender_id = 211
flag = '01111110'

class ClientThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def convert_id_to_binary(self, id_value):
        # Convert ID to binary representation
        return format(id_value, '08b')

    def bit_stuffing(self, data):
        stuffed_data = ""
        consecutive_ones = 0
        for bit in data:
            if bit == '1':
                consecutive_ones += 1
            else:
                consecutive_ones = 0

            stuffed_data += bit
            if consecutive_ones == 5:
                stuffed_data += '0'
                consecutive_ones = 0

        return stuffed_data

    def run(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 12346
        try:
            client.connect((host, port))
        except ConnectionRefusedError:
            self.message_received.emit("Failed to connect: Connection refused.")
            return
        except Exception as e:
            self.message_received.emit(f"Failed to connect: {str(e)}")
            return

        while True:
            data_to_send = input("Enter words to be sent (Enter 'q' to quit): ")
            if data_to_send.lower() == 'q':
                break

            # Convert sender and receiver IDs to binary
            sender_binary = self.convert_id_to_binary(sender_id)
            receiver_binary = self.convert_id_to_binary(receiver_id)

            # Form the header by concatenating sender and receiver IDs
            complete_header = flag + sender_binary + receiver_binary

            # Convert each word to binary and apply bit stuffing
            for word in data_to_send.split():
                words_binary = self.bit_stuffing(''.join(format(ord(x), '08b') if len(x) == 1 and x != ' ' else '') for x in word)

                # Combine flag, header, sender and receiver IDs, and stuffed data for each word
                complete_data = complete_header + words_binary + flag

                # Logic to send complete binary data to the server
                client.send(complete_data.encode())

        client.close()

class SecondPage(QWidget):
    def __init__(self, client_thread, parent=None):
        super(SecondPage, self).__init__(parent)
        self.client_thread = client_thread
        self.layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.send_button)

        self.binary_output = QTextEdit()
        self.binary_output.setReadOnly(True)
        self.layout.addWidget(self.binary_output)

        self.setLayout(self.layout)

    def send_message(self):
        message = self.input_text.toPlainText()

        print("Message sent to server:", message)

        # Convert the sender and receiver IDs to binary
        sender_binary = format(sender_id, '08b')
        receiver_binary = format(receiver_id, '08b')

        # Convert each word in the input message to binary and apply bit stuffing
        for word in message.split():
            words_binary = self.client_thread.bit_stuffing(''.join(format(ord(x), '08b') if len(x) == 1 and x != ' ' else '') for x in word)

            # Combine flag, header, sender and receiver IDs, and stuffed data for each word
            complete_data = flag + sender_binary + receiver_binary + words_binary + flag

            # Display stuffed binary data in the GUI, including the flag, header, and stuffed data for each word
            header_output = f"Header (including flag): {flag + sender_binary + receiver_binary + flag}\n"
            complete_output = header_output + f"Binary Equivalent (after bit stuffing) for each word: {words_binary}\n"
            self.binary_output.append(complete_output)

            # Logic to send complete binary data to the server
            client.send(complete_data.encode())

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client")
        self.setGeometry(100, 100, 600, 400)

        self.client_thread = ClientThread()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.connect_button = QPushButton("Connect to Server")
        self.connect_button.clicked.connect(self.start_client)
        self.layout.addWidget(self.connect_button)

        self.stuffed_data_output = QTextEdit()
        self.stuffed_data_output.setReadOnly(True)
        self.layout.addWidget(self.stuffed_data_output)

        self.client_output = QTextEdit()
        self.client_output.setReadOnly(True)
        self.layout.addWidget(self.client_output)

        self.central_widget.setLayout(self.layout)
        self.second_page = SecondPage(self.client_thread, self)
        self.client_thread.message_received.connect(self.update_server_output)

    def update_server_output(self, message):
        self.client_output.append(message)

    def start_client(self):
        self.client_output.clear()
        self.stuffed_data_output.clear()
        self.client_thread.start()
        self.switch_to_second_page()

    def switch_to_second_page(self):
        self.setCentralWidget(self.second_page)

    def closeEvent(self, event):
        # Override closeEvent to ensure the client socket is closed
        global client
        client.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_window = ClientWindow()
    client_window.show()
    sys.exit(app.exec_())

