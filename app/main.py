import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket = socket.create_server(("localhost", 4221))
    # wait for client

    #server_socket.accept() waits for the client and when the client joins the http server it returns the client IP and a TCP connection pipe to the client for information transport 
    while True:
      connection , address = server_socket.accept()
      request = connection.recv(1024) #this request arrives in bytes
      request_txt = request.decode()  #we can decode this request to understandable text
      request_line = request_txt.split("\r\n")[0]

      method , path , version = request_line.split(" ")

      print(request_line)

      if (path=='/'):
           OKresponse = b"HTTP/1.1 200 OK\r\n\r\n"
           connection.sendall(OKresponse)
      else:
           Error_response = b"HTTP/1.1 404 Not Found\r\n\r\n"
           connection.sendall(Error_response)
    
      connection.close()
    # server_socket.accept()


if __name__ == "__main__":
    main()
