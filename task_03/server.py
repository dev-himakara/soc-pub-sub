"""
Task 3 - Server Application
============================
A TCP socket server that handles Topic-Based Publish/Subscribe routing.
Clients send a handshake: `ROLE:<role>,TOPIC:<topic>`
Messages from Publishers are routed ONLY to Subscribers on the exact same topic.

Usage:
    python3 server.py <PORT>
"""

import socket
import sys
import threading
from collections import defaultdict

# Dictionaries mapping TOPIC string to a list of connected sockets
subscribers = defaultdict(list)
publishers = defaultdict(list)
clients_lock = threading.Lock()

def broadcast_to_topic(topic, message, sender_address):
    """Send a message to all connected subscribers of a specific topic."""
    with clients_lock:
        topic_subs = subscribers.get(topic, [])
        # Iterate over a copy to allow removing dead sockets
        for sub_socket in list(topic_subs):
            try:
                sub_socket.sendall(message.encode("utf-8"))
            except Exception as e:
                print(f"[SERVER] Error sending to a {topic} subscriber: {e}")
                subscribers[topic].remove(sub_socket)
                sub_socket.close()

def handle_client(client_socket, client_address):
    """Handle communication with a single client."""
    print(f"[SERVER] New connection from {client_address[0]}:{client_address[1]}")
    client_role = "UNKNOWN"
    client_topic = "UNKNOWN"

    try:
        # Handshake: e.g. "ROLE:PUBLISHER,TOPIC:WEATHER"
        handshake_data = client_socket.recv(1024).decode("utf-8").strip()
        
        try:
            # Parse the handshake string
            parts = handshake_data.split(",")
            role_part = parts[0].split(":")[1].strip().upper()
            topic_part = parts[1].split(":")[1].strip().upper()
            
            client_role = role_part
            client_topic = topic_part
        except Exception:
            print(f"[SERVER] Invalid handshake from {client_address}: {handshake_data}")
            client_socket.close()
            return

        # Register the client
        with clients_lock:
            if client_role == "PUBLISHER":
                publishers[client_topic].append(client_socket)
                print(f"[SERVER] {client_address} registered as PUBLISHER on {client_topic}.")
            elif client_role == "SUBSCRIBER":
                subscribers[client_topic].append(client_socket)
                print(f"[SERVER] {client_address} registered as SUBSCRIBER on {client_topic}.")
            else:
                print(f"[SERVER] Unknown role '{client_role}' from {client_address}.")
                client_socket.close()
                return

        # Listen for messages
        while True:
            data = client_socket.recv(4096)
            if not data:
                print(f"[SERVER] [{client_role}|{client_topic}] {client_address} disconnected.")
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "terminate":
                print(f"[SERVER] [{client_role}|{client_topic}] {client_address} sent 'terminate'.")
                break

            print(f"[{client_role}|{client_topic}|{client_address}] {message}")

            # Route message if it came from a publisher
            if client_role == "PUBLISHER":
                # Prefix message with topic for clarity on the subscriber side
                formatted_message = f"[{client_topic}] {message}"
                broadcast_to_topic(client_topic, formatted_message, client_address)

    except ConnectionResetError:
        print(f"[SERVER] [{client_role}|{client_topic}] {client_address} disconnected abruptly.")
    except Exception as e:
        print(f"[SERVER] Error handling {client_address}: {e}")
    finally:
        # Cleanup
        with clients_lock:
            if client_role == "PUBLISHER" and client_socket in publishers[client_topic]:
                publishers[client_topic].remove(client_socket)
            elif client_role == "SUBSCRIBER" and client_socket in subscribers[client_topic]:
                subscribers[client_topic].remove(client_socket)
        client_socket.close()
        print(f"[SERVER] Connection to {client_address} closed.")

def start_server(port):
    """Start the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(5)
        print(f"[SERVER] Topic-Based Pub/Sub Server listening on port {port}...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down server (Ctrl+C).")
    finally:
        server_socket.close()
        print("[SERVER] Server offline.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <PORT>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid port number.")
        sys.exit(1)

    start_server(port)
