# COM-Server

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jonyboi396825/COM-Server/Run%20Pytest%20(Push%20to%20master))
[![Documentation Status](https://readthedocs.org/projects/com-server/badge/?version=latest)](https://com-server.readthedocs.io/en/latest/?badge=latest)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jonyboi396825/COM-Server/Upload%20Python%20Package?label=PyPI%20upload)
![PyPI](https://img.shields.io/pypi/v/com_server?label=Version)

COM-Server is a Python library and a local web server that hosts an API locally and interacts with serial or COM ports. The Python library provides a different way of sending and receiving data from the serial port using a thread, and it also gives a set of tools that simplifies the task of manipulating data to and from the port. Additionally, the server makes it easier for other processes to communicate with the serial port.

The serial communication uses [pyserial](https://pyserial.readthedocs.io/en/latest/pyserial.html) as its back-end and the server uses [flask-restful](https://flask-restful.readthedocs.io/en/latest/quickstart.html) and [Flask](https://flask.palletsprojects.com/en/2.0.x/). Reading their documentations may help with developing with COM-Server.

**NOTE**: COM-Server has only been tested on:  
Operating systems:

- Ubuntu 20.04 (Focal Fossa)
- Raspberry Pi OS 10 (Buster)
- Mac OS 10.15.x (Catalina)
- Mac OS 11.6 (Big Sur)
- Windows 10

Python versions:

- Python 3.7.2
- Python 3.7.3
- Python 3.8.10
- Python 3.9.7
- Python 3.10.0

Serial ports:

- Arduino UNO
- Arduino Nano

## Recommended use
COM-Server is **not** meant to be used like a normal JSON API, even though it uses Flask and Flask-restful. If there are many different devices accessing the endpoints at the same time, data will be backed up, since the serial communication is relatively slow and things cannot be sent to the serial device at the same time. 

The server is recommended to be used like a socket, and it should be used as a way for another process (should be only one; COM-Server has no implemented synchronization) on one computer (could be the same computer or another one on the same network) to communicate with the serial port via `pyserial` and this Python program. 
 

## Installation

**NOTE**: COM-Server only works on Python >= 3.6.

Using [pip](https://pip.pypa.io/en/stable/getting-started/):
```sh
> pip install -U com-server
```

For beta releases, use the `--pre` option:
```sh
> pip install --pre com-server
```

## Quickstart

```py
# launches a development server on http://0.0.0.0:8080

import com_server
from com_server.api import Builtins

conn = com_server.Connection(<baud>, "<serport>") 
handler = com_server.RestApiHandler(conn) 
Builtins(handler) 

handler.run_dev(host="0.0.0.0", port=8080) 

conn.disconnect()
```
Replace "&lt;serport&gt;" and "&lt;baud&gt;" with the serial port and baud rate.

Alternatively, you can use the command line:
```sh
> com_server run <baud> <serport>
```
Again, replace "&lt;serport&gt;" and "&lt;baud&gt;" with the serial port and baud rate.

## Links:  
- Documentation: [https://com-server.readthedocs.io/en/latest/](https://com-server.readthedocs.io/en/latest/)
- Source code: https://github.com/jonyboi396825/COM-Server
- Issue tracker: https://github.com/jonyboi396825/COM-Server/issues
- Contributing: [https://github.com/jonyboi396825/COM-Server/blob/master/CONTRIBUTING.md](https://github.com/jonyboi396825/COM-Server/blob/master/CONTRIBUTING.md)
- Changelog: [https://github.com/jonyboi396825/COM-Server/blob/master/CHANGELOG.md](https://github.com/jonyboi396825/COM-Server/blob/master/CHANGELOG.md)
