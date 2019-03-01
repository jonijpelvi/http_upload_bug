import socket
from http_class import HTTP
import os
import struct
from http_request_class import Request
http = HTTP()
request_handler = Request(".\\root", "index.html")
upload_file_path = ".\\root\\uploads\\"

IP = "192.168.1.154"
port = 80


def post_request_check(request):
    if request.split("/")[-2] == "uploads":
        return True
    else:
        return False


def handle_upload_file(file_path, client_sock):
    file_path = upload_file_path + file_path.split("/")[-1]
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        client_sock.send(struct.pack("<I", len(data)))
        client_sock.send(data)
    else:
        client_sock.send("HTTP/1.1 ImageNotFound")


def handle_request(client_sock):
    if http.get_check_request(client_sock):
        if http.request[0] == "GET":
            if http.request[1].split("/")[-2] == "uploads":
                handle_upload_file(http.request[1], client_sock)
            else:
                request_handler.take_request(http.request)
                request_handler.check_get_send(client_sock)
        elif http.request[0] == "POST":
            if post_request_check(http.request[1]):
                name_file = http.request[1].split("/")[-1]
                image = ""
                data_len = struct.unpack("<I", client_sock.recv(4))  # BUG
                print(data_len)
                while len(image) < data_len:
                    image += client_sock.recv(1024)
                with open(upload_file_path + name_file, 'wb') as f:
                    f.write(image)
                client_sock.send("The image successfully uploaded as " + str(name_file))
            else:
                client_sock.send("HTTP/1.1 404(NotFound)")


def main():
    sock = socket.socket()
    sock.bind((IP, port))
    sock.listen(25)
    while True:
        print("Awaiting Connection...")
        client_sock, addr = sock.accept()
        print("Connection established!")
        handle_request(client_sock)
        print("Closing connection.")
        client_sock.close()


if __name__ == "__main__":
    main()
