# Task 2: Publishers and Subscribers

This directory contains the solution for **Task 2** of the Publish/Subscribe middleware assignment.

## Objective
Extend the basic client-server implementation (from Task 1) to support **multiple concurrent clients**, and introduce two specific roles:
* **Publisher**: A client that sends messages.
* **Subscriber**: A client that receives messages.

The server acts as a central broker. When it receives a message from a Publisher, it routes (broadcasts) that message to all currently connected Subscribers.

## Features Implemented
* **Multi-threading on Server**: The server uses Python's `threading` module to accept and handle multiple clients concurrently without blocking.
* **Role Handshake**: When a client connects, the first message it sends is a handshake string (`ROLE:PUBLISHER` or `ROLE:SUBSCRIBER`) so the server knows how to treat it.
* **Message Routing**: Publishers can send messages, but they don't receive anything. Subscribers run a background thread to continuously listen for and display messages forwarded by the server.

---

## How to Run

### 1. Start the Server
Open a terminal and run the server by providing a PORT number (e.g., `5000`):
```bash
python3 server.py 5000
```
*The server will start listening for incoming connections.*

### 2. Start a Subscriber Client
Open a second terminal and start a subscriber. You must provide the Server IP, Port, and Role (`SUBSCRIBER`):
```bash
python3 client.py 127.0.0.1 5000 SUBSCRIBER
```
*(You can start as many subscribers in separate terminals as you want).*

### 3. Start a Publisher Client
Open a third terminal and start a publisher. Provide the Server IP, Port, and Role (`PUBLISHER`):
```bash
python3 client.py 127.0.0.1 5000 PUBLISHER
```
*(You can also start multiple publishers if you wish).*

### 4. Test the Pub/Sub Messaging
* Type a message in the **Publisher** terminal and press Enter.
* You will instantly see that message appear on all running **Subscriber** terminals.
* Check the **Server** terminal to see logs of connections, roles, and message routing.

### 5. Terminate
Type `terminate` in any client (Publisher or Subscriber) to gracefully disconnect it from the server.
You can press `Ctrl+C` on the server terminal to shut down the server entirely.

---

## File Breakdown
* `server.py`: Listens for connections. Maintains a thread-safe list of connected Publishers and Subscribers using `threading.Lock()`. Routes messages from publishers to subscribers.
* `client.py`: Connects to the server, sends its role on startup, and utilizes a background thread (`receive_messages`) to continuously listen to incoming traffic (necessary for subscribers).
