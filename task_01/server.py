"""
Task 1 - Server Application
============================
A TCP socket server that listens on a specified PORT,
accepts a client connection, and displays received messages
on the server terminal.

Usage:
    python3 server.py <PORT>

Example:
    python3 server.py 5000
"""

import socket
import sys


def start_server(port):
    """Start the TCP server on the given port."""

    # Create a TCP socket (IPv4, Stream)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow port reuse so we can restart the server quickly
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all available interfaces on the specified port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections (backlog of 1 for Task 1)
    server_socket.listen(1)
    print(f"[SERVER] Listening on port {port}...")
    print(f"[SERVER] Waiting for a client to connect...\n")

    try:
        # Accept a single client connection
        client_socket, client_address = server_socket.accept()
        print(f"[SERVER] Client connected from {client_address[0]}:{client_address[1]}\n")

        # Receive messages in a loop
        while True:
            # Receive data (up to 4096 bytes)
            data = client_socket.recv(4096)

            # If no data is received, the client has disconnected
            if not data:
                print("\n[SERVER] Client disconnected (connection lost).")
                break

            # Decode the received bytes to a string
            message = data.decode("utf-8").strip()

            # Check if the client sent the terminate signal
            if message.lower() == "terminate":
                print(f"\n[SERVER] Client sent 'terminate'. Closing connection.")
                break

            # Display the received message on the server terminal
            print(f"[CLIENT] {message}")

        # Close the client connection
        client_socket.close()
        print("[SERVER] Client connection closed.")

    except KeyboardInterrupt:
        print("\n[SERVER] Server interrupted by user (Ctrl+C).")

    finally:
        # Close the server socket
        server_socket.close()
        print("[SERVER] Server shut down.")


if __name__ == "__main__":
    # Validate command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <PORT>")
        print("Example: python3 server.py 5000")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid port number.")
        sys.exit(1)

    if not (1024 <= port <= 65535):
        print(f"Error: Port must be between 1024 and 65535. Got {port}.")
        sys.exit(1)

    start_server(port)
