# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import time
import urllib2
import urllib

from .constants import BASE_URL
from .constants import ERROR_LEVEL_CRITICAL
from .user_communication import show_message

DOWNLOAD_LIMIT = 1000
PAYLOAD_FORMAT = "json"
TASK_STATUS_PENDING = "PENDING"
TASK_STATUS_SUCCESS = "SUCCESS"
TASK_STATUS_FAILURE = "FAILURE"
TASK_INTERVAL_MIN = 0.25
TASK_INTERVAL_INCREMENT = 0.25
TASK_INTERVAL_MAX = 5


def retrieve_data_from_lizard(username, password, asset_type, payload):
    """
    Function to get the JSON with asset data from the Lizard API.

    Args:
        (str) asset_type: Get data from the Lizard API from this
                          asset type.
        (dict) payload: A dictionary containing a possible payload add to
                        the API call.
        (str) username: The username of the Lizard account.
        (str) password: The password of the Lizard account.

    Returns:
        (dict) data: A data dictionary containing the
                     asset type (data['asset_type']),
                     max_amount of results (data['max_amount']),
                     list of assets (data['list_of_assets']),
                     error_message (data['error_message'])
    """
    # Download all the assets of an asset type
    max_amount = get_max_amount(username, password, asset_type, payload)
    payload["async"] = "true"
    payload["format"] = PAYLOAD_FORMAT
    payload["page_size"] = DOWNLOAD_LIMIT
    payload["page"] = 1
    current_amount = 0
    results = []
    queue_time_interval = TASK_INTERVAL_MIN
    error_message = ""
    data = {
        "asset_type": asset_type,
        "max_amount": max_amount,
        "list_of_assets": results,
        "error_message": error_message
    }

    while current_amount < max_amount:
        # show_message("Downloading {}...".format(asset_type))
        # Create a task to download the JSON async
        task_start_url = "{}{}/".format(BASE_URL, asset_type)
        task_start_json = send_request(
            task_start_url, username, password, payload)

        # Get the task JSON
        task_payload = {"format": "json"}
        task_url = "{}".format(task_start_json["url"])
        task_json = send_request(task_url, username, password, task_payload)

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
            try:
                for result in result_json["results"]:
                    results.append(result)
            except KeyError:
                return
            # Get the results from the JSON
            current_amount += DOWNLOAD_LIMIT
            payload["page"] += 1
        elif task_status == TASK_STATUS_FAILURE:
            data["error_message"] = "Task failure."
            return data
        else:
            data["error_message"] = "Uncaught task status: {}.".format(
                task_status)
            return data

    # Return the data
    data["list_of_assets"] = results
    return data


def get_max_amount(username, password, asset_type, payload):
    """
    Function to get the max amount of assets of an asset type.

    In this function, the count property of max_amount_data is the maximum
    amount of that asset type. A small request is done to the API to return
    this amount.
    username is the username used for logging into Lizard.
    password is the password used for logging into Lizard.
    """
    payload["format"] = PAYLOAD_FORMAT
    payload["page_size"] = 1
    url = BASE_URL + asset_type
    max_amount_json = send_request(
        url, username, password, payload)
    max_amount = max_amount_json["count"]
    return max_amount


def send_request(url, username, password, payload=None):
    """
    Send a request to the Lizard API.

    Args:
        (str) url: The url to request. If a payload is added as argument,
                        it will be encoded and added to the url.
        (str) username: The username used for logging into Lizard.
        (str) password: The password used for logging into Lizard.
        (dict) payload: Optional. Payload to add to the request.

    Returns:
        (json) json_: JSON with the results of the request.
    """
    # Encode the payload and add to the base_url.
    if payload is not None:
        payload_encoded = urllib.urlencode(payload)
        url = "{}?{}".format(url, payload_encoded)
    # Send the request
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
