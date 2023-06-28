
# Cyber Security Project - Digital Certificate Simulation

This project is a simplified implementation of a cyber security system that aims to help users understand how digital certificates work. It includes a client-side application for sending certificate requests and a server-side application for receiving, validating, and generating certificates. The project is developed in Python, utilizing RSA encoding (implemented from scratch) and the Socket library for network communication.

## Project Overview

The main goal of this project is to simulate the process of requesting and generating digital certificates. Digital certificates are a fundamental aspect of secure communication on the internet, as they validate the authenticity of entities and enable secure encryption. By creating this project, users can gain a better understanding of the inner workings of digital certificates and the associated cryptographic techniques.

## Project Components

This project consists of two main components:

### Client-side Application

The client-side application allows users to generate certificate requests and send them to the server for validation and certificate generation. The client application performs the following tasks:

- Generates a certificate request using RSA encoding.
- Sends the certificate request to the server for validation.
- Receives and verifies the generated certificate from the server.
- Stores the received certificate securely.

### Server-side Application

The server-side application receives certificate requests from clients, validates them, and generates digital certificates. The server application performs the following tasks:

- Listens for incoming certificate requests from clients.
- Validates the certificate request received from the client.
- Generates a digital certificate using RSA encoding.
- Sends the generated certificate to the client for secure storage.


---

Thank you for exploring this cyber security project! If you have any questions or feedback, please feel free to reach out. Happy learning and exploring the world of digital certificates and encryption!
