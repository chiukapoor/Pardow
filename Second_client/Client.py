"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import math
import json
import requests

fields = ('Host', 'Port')


def threads(e):
    addr = (e['Host'].get(), int(e['Port'].get()))

    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(addr)

    receive_thread = Thread(target=clientReceive())
    receive_thread.start()
    receive_thread.join()


def Handler(start, end, url, filename, startServer):
    # specify the starting and ending of the file
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    # Requesting the file from server
    reqfile = requests.get(url, headers=headers, stream=True)
    # Checking for status code
    if reqfile.status_code == 206:
        # Saving the content inside the file
        with open(filename, 'r+b') as f:
            seek = int(start-startServer)
            f.seek(seek)
            f.write(reqfile.content)
    else:
        output.insert(END, "Download in parts not Supported")


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
    output.insert(END, str(round(file_size/(1024*1024), 3))+"MB")
    fp = open(file_name, "wb")
    fp.write(('\0' * file_size).encode())
    fp.close()
    # Defining the number of threads
    number_of_threads = 4
    threads = []
    part = math.floor(file_size / number_of_threads)
    start = startServer
    end = start + part
    for i in range(number_of_threads):
        # Passing the arguments and creating a Thread
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

    output.insert(END, '%s downloaded' % file_name)
    output.insert(END, 'Sending the file to the server!')
    with open(file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data:
            client_socket.send(data)
            data = f.read(CHUNK_SIZE)
    output.insert(END, "File send to the server!")


def makeform(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    entries['Host'].insert(0, "127.0.0.1")
    entries['Port'].insert(0, "3300")
    return entries


if __name__ == "__main__":
    # Defining the chunk size
    CHUNK_SIZE = 4096

    # Tk module started
    win = Tk()

    # Different Frame initiated
    topFrame = Frame(win)
    topFrame.pack()
    midFrame = Frame(win)
    midFrame.pack()
    bottFrame = Frame(win)
    bottFrame.pack()

    # Title and Geometry of GUI
    win.title("Pardow")
    win.geometry("350x350+30+30")

    # Top bar Menu
    menu = Menu(win)
    win.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New')
    filemenu.add_command(label='Open...')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=win.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

    # Making the entry form
    ents = makeform(topFrame, fields)

    # Go and Close button
    b1 = Button(midFrame, text='Go', command=(lambda e=ents: threads(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(midFrame, text='Quit', command=win.quit)
    b3.pack(side=LEFT, padx=5, pady=5)
    win.bind('<Return>', (lambda event, e=ents: threads(e)))

    # Output Area
    scrollbar = Scrollbar(bottFrame)
    output = Listbox(bottFrame, height=15, width=50, yscrollcommand=scrollbar.set)
    output.pack(side=LEFT, fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=Y)
    win.mainloop()
