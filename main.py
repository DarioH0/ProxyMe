import socket
import threading
import requests
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from http.client import HTTPConnection
from http import HTTPStatus
from urllib.parse import urlparse

def handle_client(client_socket, proxy_type):
    try:
        if proxy_type in ["http", "https"]:
            handle_http(client_socket, proxy_type)
        elif proxy_type == "socks4":
            handle_socks4(client_socket)
        elif proxy_type == "socks5":
            handle_socks5(client_socket)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def handle_http(client_socket, proxy_type):
    request_data = client_socket.recv(4096)
    request_str = request_data.decode('utf-8')
    print(f"HTTP Request:\n{request_str}")

    # Parse the request to get the target URL
    first_line = request_str.split('\n')[0]
    method, url, _ = first_line.split()
    parsed_url = urlparse(url)

    # Construct the proxy URL
    proxy_url = f"{proxy_type}://{parsed_url.netloc}{parsed_url.path}"
    
    # Forward the request
    response = requests.request(method, proxy_url, headers={'Host': parsed_url.netloc}, data=request_data, stream=True)
    
    # Send the response back to the client
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            client_socket.sendall(chunk)

def handle_socks4(client_socket):
    print('Not available. Try HTTP/S')

def handle_socks5(client_socket):
    print('Not available. Try HTTP/S')

def start_proxy(proxy_type, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", port))
        server.listen(5)

        print(f"Proxy server listening on {proxy_type} port {port}")

        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"Proxy IP address: {ip_address}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket, proxy_type))
            client_handler.start()
    except Exception as e:
        print(f"Error starting proxy server: {e}")
        server.close()
    except KeyboardInterrupt:
        print("Proxy server shutting down.")
        server.close()

if __name__ == "__main__":
    try:
        proxy_type = input("Select proxy type (http, https, socks4, socks5): ").lower()
        proxy_port = int(input("Enter the port for the proxy server: "))
        
        if proxy_type not in ["http", "https", "socks4", "socks5"]:
            print("Invalid proxy type. Please select a valid option.")
            exit(1)

        print("Proxy server starting...")
        start_proxy(proxy_type, proxy_port)
    except ValueError:
        print("Invalid port number. Please enter a valid integer.")
