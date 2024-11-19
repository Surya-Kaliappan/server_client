Zero Knowledge Proof for Data Privacy
Project Overview
This project demonstrates a basic Zero-Knowledge Proof (ZKP) for secure communication and data privacy using SSL/TLS encryption. It includes a client-server architecture where communication between the client and the server is encrypted and secure, ensuring that sensitive data is not exposed. The client connects to the server, sends messages, and receives responses in a chat-like environment.

The server handles multiple clients concurrently and uses SSL/TLS encryption for secure data transmission. The client has a graphical interface built with Tkinter in Python, which allows users to enter their username, send messages, and view messages in real-time.

Features
Client-Server Communication: Real-time messaging between the client and the server.
SSL/TLS Encryption: Secure communication between the client and the server using SSL/TLS certificates.
Username-based Authentication: Clients provide a username for identification.
Real-time Message Updates: Messages are displayed in real-time in the client's graphical interface.
Group Strength Indicator: Displays the number of active users in the chat.
Theme Toggle: Ability to switch between light and dark themes in the client interface.
Requirements
Before running the project, ensure that you have the following requirements:

OpenSSL Commands
To generate SSL/TLS certificates for secure communication, use the following OpenSSL commands:

Generate a private key with encryption: 'openssl genrsa -aes256 -out private.key 2048'
Remove the passphrase from the private key: 'openssl rsa -in private.key -out private.key'
Generate a self-signed certificate (valid for 100 years): 'openssl req -new -x509 -nodes -sha1 -key private.key -out certificate.crt -days 36500'
Create a PEM file with the self-signed certificate: 'openssl req -x509 -new -nodes -key private.key -sha1 -days 36500 -out new.pem'

Dependencies
Python 3.x
Tkinter (for GUI)
ssl module (for secure sockets)
socket module (for communication)

Files Included
server.py: Python code for the server-side application. It accepts client connections, handles multiple clients simultaneously, and uses SSL/TLS for secure communication.
client.py: Python code for the client-side application. It provides a graphical user interface (GUI) using Tkinter for the user to interact with the chat.

*Running the Application

Server Side
To run the server, execute the following command: 'python server.py'

Client Side
To run the client, execute the following command: 'python client.py'
