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


def get_data(dockwidget, asset_type):
    """Function to get the JSON with asset data from the Lizard client."""
    # Download all the assets of an asset type
    max_amount = get_max_amount(asset_type)
    payload = {"async": "true", "format": PAYLOAD_FORMAT,
               "page_size": DOWNLOAD_LIMIT, "page": 1}
    current_amount = 0
    results = []

    while current_amount < max_amount:
        # Create a task to download the JSON async
        payload_encoded = urllib.urlencode(payload)
        task_start_url = "{}{}/?{}".format(
            BASE_URL, asset_type, payload_encoded)
        task_start_response = urllib2.urlopen(task_start_url)
        task_start_data = json.load(task_start_response)

        # Get the task JSON
        task_payload = {"format": "json"}
        task_payload_encoded = urllib.urlencode(task_payload)
        task_url = "{}?{}".format(task_start_data["url"], task_payload_encoded)
        task_response = urllib2.urlopen(task_url)
        task_data = json.load(task_response)

        # Check whether the task is done
        task_status = str(task_data["task_status"])
        while task_status == TASK_STATUS_PENDING:
            # Update the task JSON
            task_response = urllib2.urlopen(task_url)
            task_data = json.load(task_response)
            task_status = str(task_data["task_status"])
            # Loop every 0.5 seconds
            time.sleep(0.5)
        if task_status == TASK_STATUS_SUCCESS:
            # Get the JSON with the data
            result_url = task_data["result_url"]
            result_response = urllib2.urlopen(result_url)
            result_data = json.load(result_response)
            for result in result_data["results"]:
                results.append(result)
        elif task_status == TASK_STATUS_FAILURE:
            dockwidget.set_all_status_bars_text("Task failure.")

        # Get the results from the JSON
        current_amount += DOWNLOAD_LIMIT
        payload["page"] += 1

    # Return the results
    return results


def get_max_amount(asset_type):
    """
    Function to get the max amount of assets of an asset type.

    In this function, the count property of max_amount_data is the maximum
    amount of that asset type. A small request is done to the API to return
    this amount.
    """
    payload = {"format": PAYLOAD_FORMAT, "page_size": 1}
    payload_encoded = urllib.urlencode(payload)
    max_amount_url = "{}{}/?{}".format(BASE_URL, asset_type, payload_encoded)
    max_amount_response = urllib2.urlopen(max_amount_url)
    max_amount_data = json.load(max_amount_response)
    max_amount = max_amount_data["count"]
    return max_amount
