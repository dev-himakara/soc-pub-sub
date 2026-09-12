"""
Task 2 - Client Application
============================
A TCP socket client that connects as a Publisher or Subscriber.
- Publishers send messages to the server.
- Subscribers receive messages from the server.
Both can type 'terminate' to exit.

Usage:
    python3 client.py <SERVER_IP> <PORT> <ROLE>

Example:
    python3 client.py 192.168.10.2 5000 PUBLISHER
    python3 client.py 192.168.10.2 5000 SUBSCRIBER
"""

import socket
import sys
import threading
import os

def receive_messages(client_socket):
    """Background thread function to receive messages from the server."""
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                # Server closed the connection
                print("\n[CLIENT] Server disconnected.")
                # We use os._exit to immediately terminate the whole process
                # since the main thread might be blocked on input()
                os._exit(0)
            
            message = data.decode("utf-8")
            print(f"\n[INCOMING] {message}\nYou: ", end="", flush=True)
    except (ConnectionAbortedError, OSError):
        # Socket was closed locally, normal termination
        pass
    except Exception as e:
        print(f"\n[CLIENT] Error receiving data: {e}")
        os._exit(1)

def start_client(server_ip, port, role):
    """Connect to the server and handle Pub/Sub communication."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[CLIENT] Connecting to {server_ip}:{port} as {role}...")
        client_socket.connect((server_ip, port))
        
        # Send handshake with role
        handshake = f"ROLE:{role}"
        client_socket.sendall(handshake.encode("utf-8"))
        print(f"[CLIENT] Connected!")
        print(f"[CLIENT] Type messages to send. Type 'terminate' to exit.\n")
        
        # Start background thread to receive messages (especially useful for Subscribers)
        receive_thread = threading.Thread(
            target=receive_messages, 
            args=(client_socket,),
            daemon=True
        )
        receive_thread.start()

        # Main thread reads user input
        while True:
            try:
                message = input("You: ")
            except EOFError:
                print("\n[CLIENT] EOF detected. Disconnecting...")
                break

            if message.strip().lower() == "terminate":
                # Send terminate to server so it closes cleanly
                client_socket.sendall(message.encode("utf-8"))
                print("[CLIENT] Terminating connection...")
                break
                
            # If we are a publisher, we send the message. 
            # If we are a subscriber, technically we shouldn't send messages, 
            # but we allow it (and server will just print them and ignore them).
            client_socket.sendall(message.encode("utf-8"))

    except ConnectionRefusedError:
        print(f"[CLIENT] Error: Could not connect to {server_ip}:{port}.")
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user (Ctrl+C).")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <SERVER_IP> <PORT> <ROLE>")
        print("Roles: PUBLISHER or SUBSCRIBER")
        sys.exit(1)

    server_ip = sys.argv[1]

    try:
        port = int(sys.argv[2])
    except ValueError:
        print(f"Error: '{sys.argv[2]}' is not a valid port number.")
        sys.exit(1)

    role = sys.argv[3].upper()
    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Error: Role must be either PUBLISHER or SUBSCRIBER.")
        sys.exit(1)

    start_client(server_ip, port, role)
