# Bit Stuffing in Client-Server Communication

This project enhances client-server communication by incorporating bit stuffing, a technique used to ensure reliable data transmission. The focus is on implementing bit stuffing in both the `ClientThread` and `SecondPage` classes.

## Theory

Bit stuffing is a technique used in data communication to ensure reliable data transmission by inserting additional bits into the data stream. This prevents more than five consecutive '1' bits, ensuring data integrity during transmission.

## Classes and Methods

### ClientThread Class

#### Bit Stuffing Method

- Implemented the `bit_stuffing` method to perform bit stuffing on binary data.
- Ensures that no more than five consecutive '1' bits are allowed.

#### Modification in `run` Method

- Applied bit stuffing to the binary representation of each word before sending it to the server.

### SecondPage Class

#### Enhanced `send_message` Method

- Incorporated bit stuffing logic into the binary conversion process before sending messages to the server.

## Execution Flow with Bit Stuffing

### ClientThread Execution

- Connects to the server and enters a loop to receive user input for messages.
- Converts sender and receiver IDs to binary and forms a header.
- Converts each word in the message to binary, applies bit stuffing, and then sends the complete binary data to the server.

### SecondPage Interaction

- Allows users to input messages through a `QTextEdit` widget.
- Converts sender and receiver IDs to binary and converts each word to binary with bit stuffing.
- Displays the binary data in the GUI for user visualization.
- Sends the complete binary data to the server, including the applied bit stuffing.

## Recommendations and Considerations

### Error Handling

- Ensure comprehensive error handling, especially in the bit stuffing process.

### User Feedback

- Maintain informative user feedback, especially in case of bit stuffing-related issues.

### Testing

- Thoroughly test the bit stuffing implementation to ensure it works as expected in various scenarios.

### Documentation and Comments

- Update comments and documentation to reflect the changes made for bit stuffing.

## How to Run

1. **Setup**:
   - Ensure you have Python and the necessary libraries installed on your system.
   - Clone the repository and navigate to the project directory.

2. **Dependencies**:
   - Install necessary dependencies. You might use `pip` to install required packages:
     ```sh
     pip install -r requirements.txt
     ```

3. **Running the Application**:
   - Execute the client and server scripts:
     ```sh
     python server.py
     python client.py
     ```

4. **Interaction**:
   - Follow the on-screen instructions to send messages from the client to the server. The messages will undergo bit stuffing before being sent.

