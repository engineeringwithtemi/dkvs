import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A1 — Socket Creation and Binding: Observations

    Throwaway experiments for topic A1. The growing system code lives in `../kvstore/server.py`. This notebook is for observing kernel/OS behavior.

    **BUILD (from curriculum):** Create a Python script that (1) creates a TCP socket, (2) binds it to localhost on a port, (3) prints the FD. Then try binding two sockets to the same port. Then try binding to port 0.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Create a TCP socket, bind it to localhost, print the FD

    Expected: an integer file descriptor (probably small, e.g. 4–10). Note that the FD belongs to *this process* — another process would get its own numbering.
    """)
    return


@app.cell
def _():
    import socket

    def create_tcp_socket(port):
      tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      tcp_socket.bind(("localhost", port))
      return tcp_socket

    def print_socket_info(socket: socket.socket):
      print("File descriptor:", socket.fileno(), "\nPort:", socket.getsockname())

    def close_socket(socket: socket.socket):
      print("Closing socket")
      socket.close()

    return close_socket, create_tcp_socket, print_socket_info


@app.cell
def _(close_socket, create_tcp_socket, print_socket_info):
    s = create_tcp_socket(2236)
    print_socket_info(s)
    close_socket(s)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Bind two sockets to the same port — observe the error

    Expected: the second `bind()` raises `OSError: [Errno 48] Address already in use` (Errno 98 on Linux). Record the exact errno + message you see.
    """)
    return


@app.cell
def _(close_socket, create_tcp_socket):
    first_socket = create_tcp_socket(2237)
    second_socket = create_tcp_socket(2237)

    close_socket(first_socket)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Bind to port 0 — observe the OS-assigned port

    Expected: `getsockname()` after `bind(('localhost', 0))` returns a port the OS chose for you, typically in the ephemeral range (49152–65535 on macOS, 32768–60999 on Linux). Run a few times and note that the port differs.
    """)
    return


@app.cell
def _(create_tcp_socket, print_socket_info):
    port_zero_socket = create_tcp_socket(0)
    print_socket_info(port_zero_socket)
    return


if __name__ == "__main__":
    app.run()
