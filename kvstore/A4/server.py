import argparse
import socket
import time

HOST = "127.0.0.1"
PORT = 65432


buffer = b""
def createTCPSocket(hostname, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((hostname, port))
    tcp_socket.listen(2)
    
    print(f"Waiting for connection")

    conn, address = tcp_socket.accept()
    buffer = bytearray()
    print(f"Connected: {address}")

    with conn:
      while True:
        line = recv_line(conn, buffer)
        if line is None:
          print(f'Peer closed connection')
          break
        print(f"Echoing {line!r} back to {address}")
        conn.send(line + b'\n')
        

def recv_line(soc: socket.socket, buffer:bytearray):
  while True:
    new_line = buffer.find(b'\n')

    if new_line != -1:
      result = buffer[:new_line]
      del buffer[:new_line+1]
      return bytes(result)
    
    data = soc.recv(1024)

    if not data:
      if buffer:
        buffer.clear()
      return None

    buffer.extend(data)
  

def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", type=int, default=5000)
  parser.add_argument("--hostname", type=str, default="localhost")
  args = parser.parse_args()

  createTCPSocket(HOST, PORT)