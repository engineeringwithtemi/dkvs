import socket

HOST = "127.0.0.1"
PORT = 65432
messages = [b"Message 1 from client", b"Message 2 from client"]

def create_tcp_client(host=HOST, port=PORT):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  sock.connect((host, port))

  with sock:
    sock.sendall(b"Message 1 from client\n")
    sock.sendall(b"Message 2 from client\n")
    sock.sendall(b"Testing on the same line\n. Isn't this wonderful.\n")

    sock.shutdown(socket.SHUT_WR)
    buffer = bytearray()
    while True:
      line = recv_line(sock, buffer)
      if not line:
        break
      print(f"Received {line!r} from {(host, port)}")

  

def recv_line(socket, buffer):
  while True:
    new_line_idx = buffer.find(b'\n')

    if new_line_idx != -1:
      line = buffer[:new_line_idx]
      del buffer[:new_line_idx+1]
      return bytes(line)

    data = socket.recv(1024)

    if not data:
      print(f"Peer closed connection. Terminating now")
      if buffer:
        buffer.clear()
      return None
    
    buffer.extend(data)


    



if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument("--port", type=int, default=5000)
  # parser.add_argument("--hostname", type=str, default="localhost")
  # args = parser.parse_args()

  # createTCPSocket(args.hostname, args.port)
  create_tcp_client()