#Importing Packages

import argparse
import requests
import json
import os
import math
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

CHUNK_SIZE = 4096

clients = {}
addresses = {}


def accept_incoming_connections(start, end, url_of_file, file_name):
    """Sets up handling for incoming clients."""
    client, client_address = SERVER.accept()
    print("%s:%s has connected." % client_address)
    addresses[client] = client_address
    data = json.dumps({"start": start, "end": end, "url": url_of_file, "filename": file_name})
    client.send(data.encode())
    chunk = client.recv(CHUNK_SIZE)
    if start == 0:
        with open(file_name, 'w+b') as f:
            f.write(chunk)
            chunk = client.recv(CHUNK_SIZE)
        f.close()

        with open(file_name, 'ab') as f:
            while chunk:
                f.write(chunk)
                chunk = client.recv(CHUNK_SIZE)
        f.close()

    else:
        with open(file_name, 'r+b') as f:
            f.seek(start)
            while chunk:
                f.write(chunk)
                chunk = client.recv(CHUNK_SIZE)

        f.close()


HOST = ''
PORT = 3300
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    #url_of_file = "https://homepages.cae.wisc.edu/~ece533/images/cat.png"
    #url_of_file = "http://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_640_3MG.mp4"

    # create a parser object
    parser = argparse.ArgumentParser(description="An app for Parallel and Distributed Download over multiple devices")

    # add argument

    parser.add_argument("-n", "--client", type=int, nargs=1, default=1,
                        help="Number of clients. Default is 2")

    parser.add_argument("-u", "--url", type=str, nargs=1, default=None,
                        help="Url of the file to be downloaded.", required=True)

    # parse the arguments from standard input
    args = parser.parse_args()
    number_of_client = args.client
    number_of_client = number_of_client[0]
    url_of_file = args.url
    url_of_file = url_of_file[0]

    file_name = url_of_file.split('/')[-1]
    i = 1
    while os.path.isfile(file_name):
        file_name = str(i)+file_name
        i += 1

    r = requests.head(url_of_file)
    file_size = int(r.headers['content-length'])
    try:
        file_size = int(r.headers['content-length'])
    except:
        print("Invalid URL")
    part = math.floor(int(file_size) / number_of_client)
    threads = []
    for i in range(number_of_client):
        start = part * i
        end = start + part
        if i == number_of_client:
            end = file_size
        ACCEPT_THREAD = Thread(target=accept_incoming_connections, kwargs={'start': start, 'end': end, 'url_of_file': url_of_file, 'file_name': file_name}).start()
        threads.append(ACCEPT_THREAD)

    print("Waiting for Downloading...")
    i = math.floor(100 / len(threads))
    for t in threads:
        t.join()
        print((int(i/2)*"#")+str(i)+"%"+(int(i/2)*"#"))
        i += i
    SERVER.close()
