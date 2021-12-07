#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests methods `send()`, `receive()`, `get()`, `get_all_rcv()`
using the server API
"""

import requests
import json
import pytest
import time

SERVER = "http://127.0.0.1:8080"

# don't start unless running
try:
    requests.get(SERVER+"/recall")
except requests.exceptions.ConnectionError:
    pytestmark = pytest.mark.skip(
        reason="Server not launched. Make sure it is running on 0.0.0.0 with port 8080, or run \"com_server -p <port> -b <baud> run\".")

def test_rcv_before_register() -> None:
    r = requests.get(SERVER + "/receive")
    assert r.status_code == 400

def test_register() -> None:
    r = requests.get(SERVER + "/register")
    assert r.status_code == 200

def test_register_after_registered() -> None:
    r = requests.get(SERVER + "/register")
    assert r.status_code == 400

class TestSendRcv:
    """
    Tests the send and receive endpoints if they are sending and receiving properly
    """

    def test_send(self) -> None:
        global send_time

        send_time = time.time()
        data = {
            "data": [1, 2, 3, 4, send_time],
            "ending": "\n",
            "concatenate": ";"
        }

        # normal test (tests send with data)
        r = requests.post(SERVER + "/send", data=data)
        loaded = json.loads(r.text)
        assert "message" in loaded and loaded["message"] == "OK"
        assert r.status_code == 200

        # tests parses correctly
        data["notanarg"] = "notanarg"
        r = requests.post(SERVER + "/send", data=data)
        loaded = json.loads(r.text)
        assert "message" in loaded
        assert r.status_code == 400

        # tests that send interval is working
        del data["notanarg"]
        r = requests.post(SERVER + "/send", data=data)
        loaded = json.loads(r.text)
        assert "message" in loaded and loaded["message"] == "Failed to send"
        assert r.status_code == 502

        time.sleep(1) # ensures that the serial data will be received in time
    
    def test_rcv(self) -> None:
        global send_time
        
        data = {
            "num_before": 0,
            "read_until": None,
            "strip": True
        }

        # tests getting to the endpoint works
        r = requests.post(SERVER + "/receive", data=data)
        loaded = json.loads(r.text)
        assert "message" in loaded and loaded["message"] == "OK" and "timestamp" in loaded and "data" in loaded
        assert r.status_code == 200

        # tests that the data received is correct
        s = f"Got: \"1;2;3;4;{send_time}\""
        assert loaded["data"] == s

class TestGet:
    """
    Tests the get and get_all endpoints
    """

    def test_get(self) -> None:
        """
        This test will send data to the send endpoint then retrieve it from
        the get endpoint; the data should match.
        """
        
        # sends to endpoint
        send_time = time.time()
        data = {
            "data": [1, 2, 3, 4, send_time],
            "ending": "\n",
            "concatenate": ";"
        }
        requests.post(SERVER+"/send", data=data)

        # gets data from endpoint
        r = requests.get(SERVER + "/get")
        loaded = json.loads(r.text)
        assert r.status_code == 200
        assert loaded["message"] == "OK"

        # tests that the data received is correct
        s = f"Got: \"1;2;3;4;{send_time}\""
        assert loaded["data"] == s
    
    def test_get_no_data(self) -> None:
        """
        Tests that the get endpoint will time out if no data
        is sent before
        """

        # gets data from endpoint
        r = requests.get(SERVER + "/get")
        loaded = json.loads(r.text)
        assert r.status_code == 502
        assert loaded["message"] != "OK"
    
    def test_get_all(self) -> None:
        """
        Tests getting all data by sending a piece of data
        and seeing if the difference in index between
        this piece of data and the one sent in TestSendRcv
        is 2 (since there was one sent in between)
        """

        global send_time

        send_time_2 = time.time()

        # sends data 2
        data = {
            "data": [1, 2, 3, 4, send_time_2],
            "ending": "\n",
            "concatenate": ";"
        }

        # normal test (tests send with data)
        r = requests.post(SERVER + "/send", data=data)

        time.sleep(1) # ensures that it is received

        # gets data
        r = requests.get(SERVER + "/receive/all")
        loaded = json.loads(r.text)

        # checks that difference in index between is 2
        s1 = f"Got: \"1;2;3;4;{send_time}\""
        s2 = f"Got: \"1;2;3;4;{send_time_2}\""

        assert loaded["data"].index(s2) - loaded["data"].index(s1) == 2

def test_unregister() -> None:
    r = requests.get(SERVER + "/recall")
    assert r.status_code == 200