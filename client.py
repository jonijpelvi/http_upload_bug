import socket
import os
from PIL import ImageGrab
import struct
IP = "192.168.1.154"
port = 80

im = ImageGrab.grab()
im.save(".\\image.jpg")
with open(".\\image.jpg", "rb") as f:
    image = f.read()

print(os.stat(".\\image.jpg").st_size)
size = struct.pack("<I", len(image))
un_size = struct.unpack("<I", size)
print(un_size)

sock = socket.socket()
sock.connect((IP, port))
sock.send("POST /uploads/image_1.jpg HTTP/1.1\r\n")
sock.send(struct.pack("<I", len(image)))  # BUG
print("struct sent")
sock.send(image)
print("image sent")
confirmation = sock.recv(1024)
print(confirmation)


sock.close()