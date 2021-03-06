# 0.2 Beta Release 1

Previous version: 0.2b0

## IMPORTANT: BREAKING changes from previous version:

- All `Connection` methods where the user can choose the return type between `str` and `bytes` now have a `return_bytes` option that defaults to False (except for `receive()`, whose `str` counterpart is still `receive_str()`), addressing [#105](https://github.com/jonyboi396825/COM-Server/issues/105)

## Changes from previous version

- Cleaned up repetitive code in `Connection`, also addressing [#105](https://github.com/jonyboi396825/COM-Server/issues/105)
- Added automatic documentation and formatted most docstrings (except for `RestApiHandler`) in Google's docstring format. Library API docs now generated using `mkdocstrings`.

# 0.2 Beta Release 0

Previous version: 0.1.*

## IMPORTANT: BREAKING changes from previous version:

- Deleted `Builtins` because of compatibility issues

## Changes from previous version

- Added logging using Python's `logging` module and also added logging to file when disconnects happen, addressing [#73](https://github.com/jonyboi396825/COM-Server/issues/73)
- CLI now runs production server instead of development server by default, and now recommending production server, addressing [#97](https://github.com/jonyboi396825/COM-Server/issues/97)
- Updated `__repr__` for `Connection`
- Added new `ConnectionRoutes` class for adding resources which gives users more flexibility over their Flask app object than the old `RestApiHandler` (check docs for more details), addressing [#104](https://github.com/jonyboi396825/COM-Server/issues/104)
- Added `start_app`, `start_conns`, `add_resources`, and `disconnect_conns` as helper functions to `ConnectionRoutes`, which allow it to start the connections and run the server.
- `ConnectionRoutes` explicitly responds with `500 Internal Server Error` rather than relying on exceptions from the `Connection` class when the connection is disconnected.
- Added the new V1 API which uses `ConnectionRoutes` and follows RESTful principles more than the V0 API, addressing [#86](https://github.com/jonyboi396825/COM-Server/issues/86)
- Fixed type annotations such that it passes `mypy` static typing checks
- Added `tox`, making CI with Github Actions easier
- CLI now uses `click` instead of `docopt` and serves V1 API
- Deleted CLI docs because help option is now better
- Updated all `Getting Started` and homepages to use `ConnectionRoutes`

# 0.1.4

Previous version: 0.1.3

## Changes from previous version

- Fixed parts of docs that were written during version 0 that were not true/very confusing and misleading

# 0.1.3

Previous version: 0.1.2

## Changes from previous version

- Fixed broken links, addressing [#92](https://github.com/jonyboi396825/COM-Server/issues/92) and [#93](https://github.com/jonyboi396825/COM-Server/issues/93)

# 0.1.2

Previous version: 0.1.1

## IMPORTANT: BREAKING changes from previous version:

- Added versioning in built-in API, addressing [#90](https://github.com/jonyboi396825/COM-Server/issues/90)

## Changes from previous version:

- Fixed return type annotation in `api_server.py`, addressing [#88](https://github.com/jonyboi396825/COM-Server/issues/88)
- Fixed dependency list in `setup.py`

# 0.1.1

Previous version: 0.1

## Changes from previous version:

- Added `q-sz` option indicating the maximum receive queue size, addressing [#81](https://github.com/jonyboi396825/COM-Server/issues/81)
- Any endpoint will now respond with `503 Service Unavailable` if another endpoint is in use by another process at the time the request is made, addressing [#80](https://github.com/jonyboi396825/COM-Server/issues/80)

# 0.1

Previous version: 0.1b1

## Changes from previous version:

- Added some more examples in the examples directory, addressing [#74](https://github.com/jonyboi396825/COM-Server/issues/74).
- Fixed [#78](https://github.com/jonyboi396825/COM-Server/issues/78) by adding thread lock to binary search method for checking availability, and also a lock to the `Connection.get_all_rcv()` and `Connection.get_all_rcv_str()` methods to **deep copy** the receive queue instead of directly returning the receive queue. 
- Added more verbose output to the disconnect handler, including that port that it reconnected to.

# 0.1 Beta Release 1

Previous version: 0.1b0

## IMPORTANT: BREAKING changes from previous version:

- Updated CLI - see [CLI docs](https://com-server.readthedocs.io/en/pre-0.1/guide/cli/) to view how the CLI now works. Previous commands may not work.
- Updated `reconnect()` method; reconnects using ports provided in `__init__()` method rather than providing a port.

## Changes from previous version:

- Fixed [#63](https://github.com/jonyboi396825/COM-Server/issues/63) by making 404 handling default behavior
- Made IO thread in `BaseConnection` abstract
- Added new endpoint `/connection_state`, getting some properties of the `Connection` object, addressing [#60](https://github.com/jonyboi396825/COM-Server/issues/60)
- Added option to remove 0.01 second delay at end of IO thread, addressing [#68](https://github.com/jonyboi396825/COM-Server/issues/68)
- `exception` in `BaseConnection` and `Connection` objects is now **DEPRECATED**
- Added disconnect handling in server (reconnects automatically, responds with `500` when disconnected)
- Cleaned up typing in source code

# 0.1 Beta Release 0

Previous version: 0.0.*

## IMPORTANT: BREAKING changes from previous version:

- Changed the way the `RestApiHandler.add_endpoint` decorator works:
    - Instead of having the decorator above a function which returns a nested class, the decorator will instead go directly above the class that extends `ConnectionResource`. To use the connection, use `self.conn` in the methods.

## Changes from previous version:

- Added the `SendQueue` and `ReceiveQueue` objects which allow the user to use  the send queues and receive queues without accidentally breaking the program
    - Added tests for these objects
- Added the ability for the user to define a custom IO thread with a connection object, the `ReceiveQueue`, and the `SendQueue` 
- Added constants for the common baud rates:
    - `NORMAL_BAUD_RATE`: 9600 bits/sec
    - `FAST_BAUD_RATE`: 115200 bits/sec
- Added the ability to initialize with multiple ports, addressing [#39](https://github.com/jonyboi396825/COM-Server/issues/39)
- Added the ability to add [cross origin resource sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) to the Flask object in the `RestApiHandler`
- Added verbose mode where the program will print arguments received from request to `stdout`
- Formatted code using [black](https://black.readthedocs.io/en/stable/index.html)
- Added more tests that actually test that the data is being sent and received correctly, addressing [#34](https://github.com/jonyboi396825/COM-Server/issues/34)
- Added a changelog to keep track of changes
