"""
Task 3 - Client Application
============================
A TCP socket client that connects as a Publisher or Subscriber
to a SPECIFIC TOPIC. 

Usage:
    python3 client.py <SERVER_IP> <PORT> <ROLE> <TOPIC>

Example:
    python3 client.py 192.168.10.2 5000 PUBLISHER TOPIC_A
    python3 client.py 192.168.10.2 5000 SUBSCRIBER TOPIC_A
"""

import socket
import sys
import threading
import os

def receive_messages(client_socket):
    """Background thread to receive routed topic messages from the server."""
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                print("\n[CLIENT] Server disconnected.")
                os._exit(0)
            
            message = data.decode("utf-8")
            print(f"\n[INCOMING] {message}\nYou: ", end="", flush=True)
    except (ConnectionAbortedError, OSError):
        pass
    except Exception as e:
        print(f"\n[CLIENT] Error receiving data: {e}")
        os._exit(1)

def start_client(server_ip, port, role, topic):
    """Connect to server and send handshake containing Role and Topic."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"[CLIENT] Connecting to {server_ip}:{port} as {role} on {topic}...")
        client_socket.connect((server_ip, port))
        
        # Send handshake with Role and Topic
        handshake = f"ROLE:{role},TOPIC:{topic}"
        client_socket.sendall(handshake.encode("utf-8"))
        print(f"[CLIENT] Connected!")
        print(f"[CLIENT] Type messages to send. Type 'terminate' to exit.\n")
        
        # Start background receiver thread
        receive_thread = threading.Thread(
            target=receive_messages, 
            args=(client_socket,),
            daemon=True
        )
        receive_thread.start()

        # Main thread reads input
        while True:
            try:
                message = input("You: ")
            except EOFError:
                print("\n[CLIENT] EOF detected. Disconnecting...")
                break

            if message.strip().lower() == "terminate":
                client_socket.sendall(message.encode("utf-8"))
                print("[CLIENT] Terminating connection...")
                break
                
            client_socket.sendall(message.encode("utf-8"))

    except ConnectionRefusedError:
        print(f"[CLIENT] Error: Could not connect to {server_ip}:{port}.")
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user (Ctrl+C).")
    finally:
        client_socket.close()
        print("[CLIENT] Disconnected.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 client.py <SERVER_IP> <PORT> <ROLE> <TOPIC>")
        print("Example: python3 client.py 127.0.0.1 5000 PUBLISHER WEATHER")
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

    topic = sys.argv[4].upper()

    start_client(server_ip, port, role, topic)
