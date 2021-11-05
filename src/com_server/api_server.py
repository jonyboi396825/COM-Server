# /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation to the HTTP server that serves
the web API for the Serial port.
"""

import typing as t

import flask
import flask_restful

from . import base_connection, connection # for typing


class EndpointExistsException(Exception):
    pass

class ConnectionResource(flask_restful.Resource):
    """A custom resource object that is built to be used with `RestApiHandler`.

    This class is to be extended and used like the `Resource` class.
    Have `get()`, `post()`, and other methods for the types of responses you need.
    """

    # functions will be implemented in subclasses

class RestApiHandler:
    """A handler for creating endpoints with the `Connection` and `Connection`-based objects.
    
    This class provides the framework for adding custom endpoints for doing
    custom things with the serial connection and running the local server
    that will host the API. It uses a `flask_restful` object as its back end. 

    Note that only one connection (one IP address) will be allowed to connect
    at a time because the serial port can only handle one process. 
    Additionally, endpoints cannot include `/register` or `recall`, as that 
    will be used to ensure that there is only one connection at a time. Finally,
    resource classes have to extend the custom `ConnectionResource` class
    from this library, not the `Resource` from `flask_restful`.
    """

    def __init__(self, conn: t.Union[t.Type[base_connection.BaseConnection], t.Type[connection.Connection]], include_builtins: bool = True, **kwargs) -> None:
        """Constructor for class

        Parameters:
        - `conn` (`Connection`): The `Connection` object the API is going to be associated with. 
        - `include_builtins` (bool) (optional): If the built-in endpoints should be included. If True, then 
        those endpoints cannot be used as custom endpoints. By default True. The built-in endpoints include:
            - `/register` (GET): An endpoint to register an IP; other endpoints will result in `400` status code
            if they are accessed without accessing this first; if an IP is already registered then this will
            result in `400`; IPs must call this first before accessing serial port 
            - `/recall` (GET): After registered, can call `/recall` to "free" IP from server, allowing other IPs to 
            call `/register` to use the serial port
            - `/send` (POST): Send something through the serial port using `Connection.send()` with parameters in request; equivalent to `Connection.send()`
            - `/receive` (GET): Respond with the most recent received string from the serial port; equivalent to `Connection.receive_str()`
            - `/get` (GET): Respond with the first string from serial port after request; equivalent to `Connection.get(str)`
            - `/send/get_first` (POST): Responds with the first string response from the serial port after sending data, with data and parameters in request; equivalent to `Connection.get_first_response()`
            - `/get/wait` (POST): Waits until connection receives string data given in request; different response for success and failure; equivalent to `Connection.wait_for_response()`
            - `/send/get` (POST): Continues sending something until connection receives data given in request; different response for success and failure; equivalent to `Connection.send_for_response()`
            - `/list_ports` (GET): Lists all available Serial ports
        
        Note that `/register` and `/recall` is reserved and cannot be used, even if `include_builtins` is False.
        - `**kwargs`, will be passed to `flask_restful.Api()`
        """

        # from above
        self.conn = conn
        self.include_builtins = include_builtins

        # flask, flask_restful
        self.app = flask.Flask(__name__)
        self.api = flask_restful.Api(self.app, **kwargs)

        # other
        self.all_endpoints = [] # list of all endpoints in tuple (endpoint str, resource class)
        self.registered = None # keeps track of who is registered; None if not registered
    
    def add_endpoint(self, endpoint: str) -> t.Callable:
        """Decorator that adds an endpoint

        This decorator needs to go above a function which
        contains a nested class that extends `ConnectionResource`.
        The function needs a parameter indicating the serial connection.
        The function needs to return that nested class.
        The class should contain implementations of request
        methods such as `get()`, `post()`, etc. similar to the 
        `Resource` class from `flask_restful`.

        For more information, see the `flask_restful` [documentation](https://flask-restful.readthedocs.io).

        Note that duplicate endpoints will result in an exception.
        If there are two classes of the same name, even in different
        endpoints, the program will append underscores to the name
        until there are no more repeats. For example, if one function
        returned a class named "Hello" and another function returned a
        class also named "Hello", then the second class name will be 
        changed to "Hello_". This happens because `flask_restful` 
        interprets duplicate class names as duplicate endpoints.

        Parameters:
        - `endpoint`: The endpoint to the resource. Cannot repeat.
        Built-in endpoints such as `/send` and `/receive` (see list in `self.__init__()`)
        cannot be used if `include_builtins` is True. Doing so will result in error.
        `/register` and `/recall` cannot be used at all, even if `include_builtins` is False.
        """

        def _checks(resource: t.Any) -> None:
            """Checks endpoint and resource"""

            # check if endpoint exists already
            check = [i for i, _ in self.all_endpoints] 
            if (endpoint in check):
                raise EndpointExistsException(f"Endpoint \"{endpoint}\" already exists")
            
            # check that resource is not None, if it is, did not return class
            if (resource is None):
                raise TypeError("function that the decorator is above must return a class")
            
            # check if resource is subclass of ConnectionResource
            if (not issubclass(resource, ConnectionResource)):
                raise TypeError("resource has to extend com_server.ConnectionResource")
            
            # check if resource name is taken, if so, change it (flask_restful interperets duplicate names as multiple endpoints)
            names = [i.__name__ for _, i in self.all_endpoints]
            if (resource.__name__ in names):
                s = f"{resource.__name__}"

                while (s in names):
                    # append underscore until no matching 
                    s += "_"
                
                resource.__name__ = s

        def _outer(func: t.Callable) -> t.Callable:
            """Decorator"""

            resource = func(self.conn) # get resource function

            # checks
            _checks(resource) # will raise exception if fails

            # req methods; _self is needed as these will be part of class functions
            def _get(_self, *args, **kwargs):
                if (not self.registered):
                    # respond with 400 if not registered
                    flask_restful.abort(400, message="Not registered; only one connection at a time")
                else:
                    return resource._get(**args, **kwargs)
            
            def _post(_self, *args, **kwargs):
                if (not self.registered):
                    # respond with 400 if not registered
                    flask_restful.abort(400, message="Not registered; only one connection at a time")
                else:
                    return resource._post(**args, **kwargs)
        
            def _head(_self, *args, **kwargs):
                if (not self.registered):
                    # respond with 400 if not registered
                    flask_restful.abort(400, message="Not registered; only one connection at a time")
                else:
                    return resource._head(**args, **kwargs)

            def _put(_self, *args, **kwargs):
                if (not self.registered):
                    # respond with 400 if not registered
                    flask_restful.abort(400, message="Not registered; only one connection at a time")
                else:
                    return resource._put(**args, **kwargs)
        
            def _delete(_self, *args, **kwargs):
                if (not self.registered):
                    # respond with 400 if not registered
                    flask_restful.abort(400, message="Not registered; only one connection at a time")
                else:
                    return resource._delete(**args, **kwargs)
                    
            # replace functions in class with new functions that check if registered
            if (hasattr(resource, "get")):
                resource._get = resource.get
                resource.get = _get
            if (hasattr(resource, "post")):
                resource._post = resource.post
                resource.post = _post
            if (hasattr(resource, "head")):
                resource._head = resource.head
                resource.head = _head
            if (hasattr(resource, "put")):
                resource._put = resource.put
                resource.put = _put
            if (hasattr(resource, "delete")):
                resource._delete = resource.delete
                resource.delete = _delete
             
            self.all_endpoints.append((endpoint, resource))
        
        return _outer
    
    def run(self, **kwargs) -> None:
        """Launches the Flask app.

        All arguments in `**kwargs` will be passed to `Flask.run()`.
        For more information, see [here](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.run).
        For documentation on Flask in general, see [here](https://flask.palletsprojects.com/en/2.0.x/)

        Some arguments include: 
        - `host`: The host of the server. Ex: `localhost`, `0.0.0.0`, `127.0.0.1`, etc.
        - `port`: The port to host it on. Ex: `5000` (default), `8000`, `8080`, etc.
        - `debug`: If the app should be used in debug mode. 
        """

        self.conn.connect() # connection Connection obj

        # register all endpoints to flask_restful
        for endpoint, resource in self.all_endpoints:
            self.api.add_resource(resource, endpoint)

        self.app.run(**kwargs) 

        self.conn.disconnect() # disconnect if stop running
