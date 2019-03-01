"""

    Request object for http server.

"""
import os


class Request:

    def __init__(self, root_path, root_file):
        self.root_folder = root_path
        self.root_file = root_file
        self.request = ""
        self.file_path = ""
        self.sent_packet = ""
        #  Headers for the packet to send.
        self.requested_file = ""
        self.content_length = ""
        self.http_header = ""
        self.content_header = ""

    def take_request(self, request):
        self.request = request
        requested_path = request[1]
        new_path = ""
        for letter in requested_path:
            if letter == "/":
                letter == "\\"
            new_path += letter
        self.file_path = self.root_folder + new_path
        if requested_path == "/":
            self.file_path = self.root_folder + "\\" + self.root_file

    def check_for_errors(self, client_sock):
        if not os.path.isfile(self.file_path):
            client_sock.send("HTTP/1.1 404(NotFound)\r\n")
            return True
        elif self.file_path.split("\\")[-1] == "403":
            client_sock.send("HTTP/1.1 403(Forbidden)\r\n")
            return True
        else:return False

    def get_requested_file(self):
        with open(self.file_path, 'rb') as f:
            self.requested_file = f.read()
        requested_file_length = str(os.stat(self.file_path).st_size)
        self.content_length = "Content-length: " + requested_file_length + "\r\n"

    def headers_creator(self):
        self.http_header = "Http/1.1 200 OK\r\n"
        content_type = self.request[1].split("\\")[-1].split(".")[-1]
        if content_type in ['jpg', 'jpeg', 'ico', 'gif']:
            self.content_header = "Content - Type: image / jpeg\r\n"

        elif content_type == "css":
            self.content_header = "Content-Type: text/css\r\n"

        elif content_type == "html":
            self.content_header = "Content-Type: text/html; charset=utf-8\r\n"

        elif content_type == "js":
            self.content_header = "Content-Type: text/javascript; charset=UTF-8\r\n"

    def packet_maker(self):
        self.sent_packet = self.http_header + self.content_length + self.content_header + "\r\n" + self.requested_file

    def check_get_send(self, client_sock):
        if not self.check_for_errors(client_sock):
            self.get_requested_file()
            self.headers_creator()
            self.packet_maker()
            client_sock.send(self.sent_packet)

    def get_post(self):
        pass
