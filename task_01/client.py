"""
Task 1 - Client Application
============================
A TCP socket client that connects to a server using
the specified IP and PORT, sends user-typed messages,
and disconnects when 'terminate' is entered.

Usage:
    python3 client.py <SERVER_IP> <PORT>

Example:
    python3 client.py 192.168.10.2 5000
"""

import socket
import sys


def start_client(server_ip, port):
    """Connect to the server and send messages."""

    # Create a TCP socket (IPv4, Stream)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        print(f"[CLIENT] Connecting to {server_ip}:{port}...")
        client_socket.connect((server_ip, port))
        print(f"[CLIENT] Connected to server at {server_ip}:{port}")
        print(f"[CLIENT] Type messages to send. Type 'terminate' to disconnect.\n")

        # Read and send messages in a loop
        while True:
            try:
                # Read user input
                message = input("You: ")
            except EOFError:
                # Handle Ctrl+D (EOF)
                print("\n[CLIENT] EOF detected. Disconnecting...")
                break

            # Send the message to the server
            client_socket.sendall(message.encode("utf-8"))

            # Check if the user wants to terminate
            if message.strip().lower() == "terminate":
                print("[CLIENT] Terminating connection...")
                break

    except ConnectionRefusedError:
        print(f"[CLIENT] Error: Could not connect to {server_ip}:{port}.")
        print("[CLIENT] Make sure the server is running.")

    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user (Ctrl+C).")

    finally:
        # Close the socket
        client_socket.close()
        print("[CLIENT] Disconnected from server.")


if __name__ == "__main__":
    # Validate command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <SERVER_IP> <PORT>")
        print("Example: python3 client.py 192.168.10.2 5000")
        sys.exit(1)

    server_ip = sys.argv[1]

    try:
        port = int(sys.argv[2])
    except ValueError:
        print(f"Error: '{sys.argv[2]}' is not a valid port number.")
        sys.exit(1)

    if not (1024 <= port <= 65535):
        print(f"Error: Port must be between 1024 and 65535. Got {port}.")
        sys.exit(1)

    start_client(server_ip, port)
