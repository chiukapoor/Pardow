"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
#import tkinter
import math
import json
import requests


CHUNK_SIZE = 4096
number_of_threads = 4


def Handler(start, end, url, filename, startServer):
    # specify the starting and ending of the file
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    # Requesting the file from server
    reqfile = requests.get(url, headers=headers, stream=True)
    # Checking for status code
    if reqfile.status_code == 206:
        # Saving the content inside the file
        with open(filename, 'r+b') as f:
            print("Start after passing" + str(start))
            print("End after passing" + str(end))
            print("StartServer after passing" + str(startServer))
            seek = start-startServer
            print(seek)
            f.seek(seek)
            f.write(reqfile.content)
    else:
        print("Download in parts not Supported")


def clientReceive():
    # Receiving the details from Server
    data = client_socket.recv(CHUNK_SIZE)
    # Decoding the JSON file
    data = json.loads(data.decode())
    startServer = data.get("start")
    endServer = data.get("end")
    url_of_file = data.get("url")
    file_name = data.get("filename")
    file_size = int(endServer)-int(startServer)
    print(file_size)
    fp = open(file_name, "wb")
    fp.write(('\0' * file_size).encode())
    fp.close()

    threads = []
    part = math.floor(file_size) / number_of_threads
    start = startServer
    end = start + part
    print(startServer)
    for i in range(number_of_threads):
        # Passing the arguments and creating a Thread
        print("Start before passing"+str(start))
        print("End before passing"+str(end))
        t = Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url_of_file, 'filename': file_name, 'startServer': startServer})
        t.setDaemon(True)
        t.start()
        threads.append(t)
        start = start + part
        end = start + part
        if i == number_of_threads-2:
            end = endServer

    for t in threads:
        t.join()

    print('%s downloaded' % file_name)
    print('Sending the file to the server!')
    with open(file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data:
            client_socket.send(data)
            data = f.read(CHUNK_SIZE)
    print("File send to the server!")


# def send(event=None):  # event is passed by binders.
#     """Handles sending of messages."""
#     msg = my_msg.get()
#     my_msg.set("")  # Clears input field.
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#         top.quit()
#
#
# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
#     send()

# top = tkinter.Tk()
# top.title("Parallel Downloader")
#
# messages_frame = tkinter.Frame(top)
# my_msg = tkinter.StringVar()  # For the messages to be sent.
# my_msg.set("Type your messages here.")
# scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# # Following will contain the messages.
# msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# msg_list.pack()
# messages_frame.pack()
#
# entry_field = tkinter.Entry(top, textvariable=my_msg)
# entry_field.bind("<Return>", send)
# entry_field.pack()
# send_button = tkinter.Button(top, text="Send", command=send)
# send_button.pack()
#
# top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
#HOST = input('Enter host: ')
#PORT = input('Enter port: ')

HOST = "127.0.0.1"
PORT = 3300
if not PORT:
    PORT = 3300
else:
    PORT = int(PORT)

BUFSIZ = 4096
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=clientReceive())
receive_thread.start()
receive_thread.join()
