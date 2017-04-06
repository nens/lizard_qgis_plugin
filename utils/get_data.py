# -*- coding: utf-8 -*-
"""Module for getting the data from the Lizard API."""
import json
import time
import urllib2
import urllib

from .constants import BASE_URL


def get_data(asset_type, payload):
    """Function to get the JSON from the Lizard client."""
    # Encode the payload
    payload_encoded = urllib.urlencode(payload)

    # Set the url
    url = "{}{}/?{}".format(BASE_URL, asset_type, payload_encoded)
    print url

    # # Get the JSON
    response = urllib2.urlopen(url)
    r = json.load(response)
    # print r  # task
    payload2 = {"format": "json"}
    payload_encoded2 = urllib.urlencode(payload2)
    task_url = "{}?{}".format(r["url"], payload_encoded2)
    # print task_url
    # follow task_url

    # # Get the JSON
    response2 = urllib2.urlopen(task_url)
    r2 = json.load(response2)
    # print r2
    # print r2["task_status"]  # PENDING
    # print type(r2["task_status"])

    while str(r2["task_status"]) == "PENDING":
        response2 = urllib2.urlopen(task_url)
        r2 = json.load(response2)
        # print r2
        time.sleep(0.5)
    if str(r2["task_status"]) == "SUCCESS":
        # print 'ja'
        # print r2  # {u'result_url': u'https://demo.lizard.net/media/downloads/da9d8f0e-1f95-4bd3-a52c-3a641d08f3e1/da9d8f0e-1f95-4bd3-a52c-3a641d08f3e1.json', u'task_id': u'da9d8f0e-1f95-4bd3-a52c-3a641d08f3e1', u'task_status': u'SUCCESS'}
        result_url = r2["result_url"]
        # print result_url  # https://demo.lizard.net/media/downloads/da9d8f0e-1f95-4bd3-a52c-3a641d08f3e1/da9d8f0e-1f95-4bd3-a52c-3a641d08f3e1.json
        # print type(result_url)  # unicode
        response3 = urllib2.urlopen(result_url)
        r = json.load(response3)
        # r = json.load(result_url.read())
        # print r
        # print type(r)
        # break
    elif str(r2["task_status"]) == "FAILURE":
        print 'FAILUREe'
    # print "m"

    # while r2["task_status"] == "PENDING":
    #     if r2["task_status"] == "SUCCES":
    #         print "SUCCES!"
    #         break
    #         return
    #     elif r2["task_status"] == "FAILURE":
    #         print "FAILURE!"
    #         break
    #         return
    #     time.sleep(1)

    response3 = r["results"]
    # count = r["count"]

    # Return the results
    return response3
