import socket  # noqa: F401
import threading

def handle_client(connection) :
   request = connection.recv(1024)
   request_txt = request.decode()  #we can decode this request to understandable text
   request_line = request_txt.split("\r\n")[0]

   print(request_line)

   method , path , version = request_line.split(" ")

   print(path)

   OK_response = b"HTTP/1.1 200 OK\r\n\r\n"
   Error404_response = b"HTTP/1.1 404 Not Found\r\n\r\n"

   if(True) :
      connection.sendall(OK_response)
      return

   if(path=="/") :
          #standard Ok response input
      connection.sendall(OK_response)
   elif(path.startswith("/echo/")):
      input_str = path[6:]
      content_len = len(input_str.encode())
      response_header = (
         #f strings are used when I need to pass a variable value inside the string , it uses {} and retruns the variable value of the variable name inside the {}
         f"HTTP/1.1 200 OK\r\n"
         f"Content-Type: text/plain\r\n"
         f"Content-Length: {content_len}\r\n"
         f"\r\n"
         f"{input_str}"
      )
      connection.sendall(response_header.encode()) #a response is always sent across encoded in bytes
   elif(path.startswith("/user-agent")):
      #a much safer and better method to slice and get the required line from the GET request
      headers = request_txt.split("\r\n")
      user_agent=""
      for header in headers:
         if(header.lower().startswith("user-agent:")):
            user_agent= header[len("User-Agent: "):]
            break

      content_len = len(user_agent.encode())

      print(f"dbg : this is user-agent : {user_agent}")

      response_header = (
         f"HTTP/1.1 200 OK\r\n"
         f"Content-Type: text/plain\r\n"
         f"Content-Length: {content_len}\r\n"
         f"\r\n"
         f"{user_agent}"
      )
      connection.sendall(response_header.encode())
   else :
      connection.sendall(Error404_response)



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
#     server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket = socket.create_server(("localhost", 4221))
    # wait for client
    

    #server_socket.accept() waits for the client and when the client joins the http server it returns the client IP and a TCP connection pipe to the client for information transport 
    while True:
      connection , address = server_socket.accept() #acknowledges the client is connected
      
      new_thread = threading.Thread(target=handle_client, args=(connection,))
      new_thread.start()

      connection.close()
         
    # server_socket.accept()


if __name__ == "__main__":
    main()
