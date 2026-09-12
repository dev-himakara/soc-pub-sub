"""
Task 2 - Server Application
============================
A TCP socket server that handles multiple concurrent clients.
Clients can be Publishers or Subscribers.
Messages from Publishers are routed to all connected Subscribers.

Usage:
    python3 server.py <PORT>

Example:
    python3 server.py 5000
"""

import socket
import sys
import threading

# Global lists to keep track of connected clients
subscribers = []
publishers = []
clients_lock = threading.Lock()

def broadcast_to_subscribers(message, sender_address):
    """Send a message to all connected subscribers."""
    with clients_lock:
        # Create a copy of the list to iterate over, in case a subscriber disconnects
        for sub_socket in list(subscribers):
            try:
                sub_socket.sendall(message.encode("utf-8"))
            except Exception as e:
                print(f"[SERVER] Error sending to a subscriber: {e}")
                # Remove dead sockets
                subscribers.remove(sub_socket)
                sub_socket.close()

def handle_client(client_socket, client_address):
    """Handle communication with a single client."""
    print(f"[SERVER] New connection from {client_address[0]}:{client_address[1]}")
    client_role = "UNKNOWN"

    try:
        # The first message should be the handshake containing the role
        handshake_data = client_socket.recv(1024).decode("utf-8").strip()
        
        if handshake_data.startswith("ROLE:"):
            client_role = handshake_data.split(":")[1].strip().upper()
            
            with clients_lock:
                if client_role == "PUBLISHER":
                    publishers.append(client_socket)
                    print(f"[SERVER] {client_address} registered as PUBLISHER.")
                elif client_role == "SUBSCRIBER":
                    subscribers.append(client_socket)
                    print(f"[SERVER] {client_address} registered as SUBSCRIBER.")
                else:
                    print(f"[SERVER] Unknown role '{client_role}' from {client_address}.")
                    client_socket.close()
                    return
        else:
            print(f"[SERVER] Invalid handshake from {client_address}. Closing connection.")
            client_socket.close()
            return

        # Receive messages in a loop
        while True:
            data = client_socket.recv(4096)
            if not data:
                print(f"[SERVER] {client_role} {client_address} disconnected (connection lost).")
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "terminate":
                print(f"[SERVER] {client_role} {client_address} sent 'terminate'.")
                break

            # Print on server CLI
            print(f"[{client_role} {client_address}] {message}")

            # Route message if it came from a publisher
            if client_role == "PUBLISHER":
                broadcast_to_subscribers(message, client_address)

    except ConnectionResetError:
        print(f"[SERVER] {client_role} {client_address} disconnected abruptly.")
    except Exception as e:
        print(f"[SERVER] Error handling {client_address}: {e}")
    finally:
        # Cleanup when client disconnects
        with clients_lock:
            if client_socket in publishers:
                publishers.remove(client_socket)
            if client_socket in subscribers:
                subscribers.remove(client_socket)
        client_socket.close()
        print(f"[SERVER] Connection to {client_address} closed.")

def start_server(port):
    """Start the TCP server to listen for multiple clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(5)
        print(f"[SERVER] Listening on port {port}...")
        
        while True:
            # Accept new connections
            client_socket, client_address = server_socket.accept()
            # Start a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address),
                daemon=True # Dies when main thread dies
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
