import socketserver
from smart_handler import SmartHomeServer

if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 5050

    with socketserver.TCPServer((HOST, PORT), SmartHomeServer) as server:
        server.serve_forever()