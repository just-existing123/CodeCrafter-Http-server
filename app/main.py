import socket  # noqa: F401
import threading
import sys 
import os
import gzip

def handle_client(connection,directory) :
   try :
    while True:
      request = connection.recv(1024)
      if not request:
         break
      request_txt = request.decode()  #we can decode this request to understandable text
      headers = request_txt.split("\r\n")
      request_line = request_txt.split("\r\n")[0]

      print(request_line)

      should_close=False
      for header in headers:
         if(header.lower().startswith("connection: ")):
            value = header[len("connection: "):]
            if(value.lower()=="close"):
               should_close=True

      method , path , version = request_line.split(" ")

      print(path)

      OK_response = b"HTTP/1.1 200 OK\r\n\r\n"
      Error404_response = b"HTTP/1.1 404 Not Found\r\n\r\n"
      Created201_response = b"HTTP/1.1 201 Created\r\n\r\n"

      if(method == "GET"):
         #the GET method
         if(path=="/") :
            #standard Ok response input
            connection.sendall(OK_response)
         elif(path.startswith("/echo/")):
            input_str = path[6:]
            content_len = len(input_str.encode())
            # response_header = (
            #   #f strings are used when I need to pass a variable value inside the string , it uses {} and retruns the variable value of the variable name inside the {}
            #   f"HTTP/1.1 200 OK\r\n"
            #   f"Content-Type: text/plain\r\n"
            #   f"Content-Length: {content_len}\r\n"
            #   f"\r\n"
            #   f"{input_str}"
            # )

            enc_format = 0
            formats = []
            for header in headers:
               if(header.lower().startswith("accept-encoding: ")):
                  formats = header[len("accept-encoding: "):].split(", ")

            for format in formats:
               if(format == "gzip"):
                  enc_format=1
                  break
         
            if(enc_format==1):
               zipped_data = gzip.compress(input_str.encode())
               #steps to compress data :
               # 1) encode the normal text/input data into binary or byte format
               # 2) the binary or byte format of the encoded data now can have mathematical repetitions which are made to collapse and remember as opening instructions for later by the compressor
               # 3) the compressed data with the mathematical instruction is shipped
               #LEGO ANALOGY FOR COMPRESSION

               content_len = len(zipped_data)

               response = (
                  f"HTTP/1.1 200 OK\r\n"
                  f"Content-Encoding: gzip\r\n"
                  f"Content-Type: text/plain\r\n"
                  f"Content-Length: {content_len}\r\n"
                  f"\r\n"
               ) 
               connection.sendall(response.encode() + zipped_data)
            else:
               response = (
                  f"HTTP/1.1 200 OK\r\n"
                  f"Content-Type: text/plain\r\n"
                  f"Content-Length: {content_len}\r\n"
                  f"\r\n"
                  f"{input_str}"
               )
               connection.sendall(response.encode()) #a response is always sent across encoded in bytes
         elif(path.startswith("/user-agent")):
           #a much safer and better method to slice and get the required line from the GET request
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
         elif(path.startswith("/files/")):
            filename = path[len("/files/"):]
            full_path = os.path.join(directory,filename)

            if(os.path.exists(full_path)):

             with open(full_path,"rb") as file:
                data = file.read()
         
             content_len = len(data)
             response_header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: application/octet-stream\r\n"
                f"Content-Length: {content_len}\r\n"
                f"\r\n"
             )

             response_bytes = response_header.encode()
             connection.sendall(response_bytes + data)
            else :
               connection.sendall(Error404_response)
         else:
             connection.sendall(Error404_response)

      elif(method=="POST"):
         #the POST method
         if(path.startswith("/files")):
            filename = path[len("/files/"):]
            full_path = os.path.join(directory,filename)

            data = request_txt.split("\r\n\r\n")[1].encode()

            with open(full_path,"wb") as file:
               #when open() is used in "w" or "wb" mode it creates a file if the file does not exist
               file.write(data)
         
            connection.sendall(Created201_response) 
         else:
            connection.sendall(Error404_response)
      
      if(should_close==True):
         closing_response = (
         f"HTTP/1.1 200 OK\r\n"
         f"Connection: close"
         f"\r\n"
         f"Thank you"
         )
         connection.sendall(closing_response.encode())
         break

   except Exception as e :
      print(f"error :{e}")
   finally:
      connection.close()



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
#     server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket = socket.create_server(("localhost", 4221))
    # wait for client
    
    directory = "."
    if(len(sys.argv)>2 and sys.argv[1]== "--directory"):
       directory = sys.argv[2]
       print(f"Serving Files from directory :{directory}")

    #server_socket.accept() waits for the client and when the client joins the http server it returns the client IP and a TCP connection pipe to the client for information transport 
    while True:
      connection , address = server_socket.accept() #acknowledges the client is connected
      
      new_thread = threading.Thread(target=handle_client, args=(connection,directory))
      new_thread.start()
         
    # server_socket.accept()


if __name__ == "__main__":
    main()
