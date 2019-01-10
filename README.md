# Pardow

Pradow is an Open Source project available for everyone to download and use with GNU V3 license.

Using the Algorithm for Distributed Computing to distribute the download parts among different PCs and latter using threads to download it Parallel in the same PC. This will increase the bandwidth usage efficiency and decrease the downloading time. Normally downloading a 3 GB file on VIT Internet which provides the speed of 300KBps Approximately takes 3 hours. If using the technique provided in the project the time taken be brought down to 2 hours including file compilation then the project can be supposed to achieve the specified objectives. Additionally, as a student is allowed to use a maximum of 10 GB per month. Multiple accounts can be used to download the 3 GB file which will at last also help in Data Usage Distribution.

### Project Modules:

The project has two major parts.
1. Server Node
2. Client Node

Server node will be the one which is responsible for segmenting the files and sending it to the client nodes for downloading. Later when the download is completed it will request those files from the client nodes to recompile them.

Client nodes will download the parts they are assigned through threading to create multiple connection and download in parallel acting as different devices on its own. This increase the overall download speed. Increase in the number of client nodes will drastically affect the increase in downloading speed. The methodlogy used is a segmented file transfer and threading.

### Working of Pardow

1. The server will first create a thread to for incoming requests of clients.
2. As soon as the client is connected the server will notify in the GUI

<p align="center">
<img src="https://github.com/C-Society/Pardow/blob/master/Misc/Pardow_Server_img.jpg" width="600" alt="Pardow Server">
</p>

3. The Client will start Downloading the file
4. When the file is Downloaded the client will send the file to the server
5. The server will combine all the files into one file

<p align="center">
<img src="https://github.com/C-Society/Pardow/blob/master/Misc/Pardow_Client_img.jpg" width="600" alt="Pardow Client">
</p>

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Author

* **Chirayu kapoor**

## License

This project is licensed under the GNU V3.0 License - see the [LICENSE](LICENSE) file for details
