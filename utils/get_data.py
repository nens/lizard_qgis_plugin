# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import time
import urllib2
import urllib

from .constants import BASE_URL

DOWNLOAD_LIMIT = 1000
PAYLOAD_FORMAT = "json"
TASK_STATUS_PENDING = "PENDING"
TASK_STATUS_SUCCESS = "SUCCESS"
TASK_STATUS_FAILURE = "FAILURE"
TASK_INTERVAL_MIN = 0.5
TASK_INTERVAL_INCREMENT = 0.5
TASK_INTERVAL_MAX = 5


def get_data(dockwidget, username, password, asset_type):
    """
    Function to get the JSON with asset data from the Lizard API.

    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    # Download all the assets of an asset type
    max_amount = get_max_amount(username, password, asset_type)
    payload = {"async": "true", "format": PAYLOAD_FORMAT,
               "page_size": DOWNLOAD_LIMIT, "page": 1}
    current_amount = 0
    results = []
    queue_time_interval = TASK_INTERVAL_MIN

    while current_amount < max_amount:
        # Create a task to download the JSON async
        task_start_url = "{}{}/".format(BASE_URL, asset_type)
        task_start_json = get_json(username, password, task_start_url, payload)

        # Get the task JSON
        task_payload = {"format": "json"}
        task_url = "{}".format(task_start_json["url"])
        task_json = get_json(username, password, task_url, task_payload)

        # Check whether the task is done
        task_status = str(task_json["task_status"])
        while task_status == TASK_STATUS_PENDING:
            # Update the task JSON
            task_json = send_request(task_url, username, password)
            task_status = str(task_json["task_status"])
            time.sleep(queue_time_interval)
            # Increase the task interval (in seconds) for bigger tasks to
            # decrease the amount of requests done
            if queue_time_interval < TASK_INTERVAL_MAX:
                queue_time_interval += TASK_INTERVAL_INCREMENT
        if task_status == TASK_STATUS_SUCCESS:
            # Get the JSON with the data
            result_url = task_json["result_url"]
            result_json = send_request(result_url, username, password)
            for result in result_json["results"]:
                results.append(result)
        elif task_status == TASK_STATUS_FAILURE:
            dockwidget.set_all_status_bars_text("Task failure.")

        # Get the results from the JSON
        current_amount += DOWNLOAD_LIMIT
        payload["page"] += 1

    # Return the results
    return results


def get_max_amount(username, password, asset_type):
    """
    Function to get the max amount of assets of an asset type.

    In this function, the count property of max_amount_data is the maximum
    amount of that asset type. A small request is done to the API to return
    this amount.
    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    payload = {"format": PAYLOAD_FORMAT, "page_size": 1}
    url = BASE_URL + asset_type
    max_amount_json = get_json(username, password, url, payload)
    max_amount = max_amount_json["count"]
    return max_amount


def get_json(username, password, base_url, payload):
    """
    Function to get a JSON from the Lizard API.

    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    payload_encoded = urllib.urlencode(payload)
    url = "{}?{}".format(base_url, payload_encoded)
    json_ = send_request(url, username, password)
    return json_


def send_request(url, username, password):
    """
    Send a request to the Lizard API.

    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    request = urllib2.Request(url)
    request = use_header(request, username, password)
    response = urllib2.urlopen(request)
    json_ = json.load(response)
    return json_


def use_header(request, username, password):
    """
    Use a header if the user is logged in with his Lizard account.

    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    if username is not None and password is not None:
        request.add_header('username', username)
        request.add_header('password', password)
    return request
