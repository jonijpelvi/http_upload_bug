""""

       HTTP object - gets http requests and send the

"""


class HTTP:

    def __init__(self):
        "root path should be the full path, if its in the same folder .\\"
        self.packet = ""  # should be the all packet with the headers.
        self.request = ""  # request should be

    def get_request(self, client_sock):
        "Get the HTTP request from the packet in a tuple, every parameter seperated, "
        packet = client_sock.recv(1024)
        self.packet = packet
        self.request = self.packet.split("\r\n")[0].split(" ")
        print("Request:" + str(self.request))

    def valid_request(self, client_sock):
        "Checks if valid request returns True/False"
        if self.request[0] == 'GET' and self.request[2] == "HTTP/1.1":
            return True
        elif self.request[0] == 'POST' and self.request[2] == "HTTP/1.1":
                return True
        else:
            client_sock.send("Invalid form of request/Unknown request.")
            print("Invalid form of request/Unknown request.")
            return False

    def get_check_request(self, client_sock):
        "Should give you a shortcut for get_request&valid_request and gice you the file path."
        self.get_request(client_sock)
        if self.valid_request(client_sock):
            return True
        else:
            return False



