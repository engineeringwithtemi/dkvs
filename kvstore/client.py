import socket
import types
import selectors
from typing import cast 

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"
PORT = 65432
messages = [b"Message 1 from client", b"Message 2 from client"]

def create_connections(host=HOST, port=PORT, num_of_con=10):
  for i in range(num_of_con):
    connid = i + 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex((host, port))
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(connid=connid, 
          total_length=sum(len(m) for m in messages),
          outb=b"", messages = messages.copy(), recv_total=0)
    sel.register(sock, events, data=data)
    print(f"Registered connid={connid!r}.")




def service_request(key, mask):
  sock = cast(socket.socket, key.fileobj)
  data = cast(types.SimpleNamespace, key.data)
  if mask & selectors.EVENT_READ:
    recv_data = sock.recv(1024)
    if recv_data:
      print(f"Received {recv_data!r} from connection {data.connid}")
      data.recv_total += len(recv_data)
    if not recv_data or data.recv_total == data.total_length:
      print(f"Closing connection from {data.connid}")
      sel.unregister(sock)
      sock.close()
  if mask & selectors.EVENT_WRITE:
    if not data.outb and data.messages:
      print(f"Echoing {data.outb!r} to {data.connid}")
      data.outb = data.messages.pop()
    if data.outb:
      print(f"Sending {data.outb!r} to connection {data.connid}")
      sent = sock.send(data.outb)
      data.outb = data.outb[sent:]


def create_conn_request():
  try:
    while True:
      events = sel.select(timeout=None)
      for key, mask in events:
        service_request(key, mask)
  except KeyboardInterrupt:
    print(f"Terminating")
  finally:
    sel.close()


if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument("--port", type=int, default=5000)
  # parser.add_argument("--hostname", type=str, default="localhost")
  # args = parser.parse_args()

  # createTCPSocket(args.hostname, args.port)
  create_connections()
  create_conn_request()