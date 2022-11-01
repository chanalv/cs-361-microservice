# Citation - the following code is adapted from and references the following documentation:
#   URL: https://zeromq.org/languages/python/
#   URL: https://requests.readthedocs.io/en/latest/
#   URL: https://www.mediawiki.org/wiki/API:Main_page

import zmq
import requests
import json

# binds REP socket to tcp://*:5555
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Server is active. Listening for requests...")
print()

while True:
    # receive search term from client
    search_term = socket.recv()
    print("Received search term from client: " + search_term.decode())

    # parameters for English Wikipedia Search API
    params = {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "exintro": "",
        "explaintext": "",
        "redirects": "1",
        "titles": search_term.decode()
    }

    # send HTTPS GET request to API Endpoint using above parameters; receive raw results
    request = requests.get("https://en.wikipedia.org/w/api.php", params=params)
    raw_results = request.json()

    print("Received raw results from Wikipedia:")
    print(raw_results)

    # send error message if Wikipedia article is not found using the user's search term
    if list(raw_results["query"].keys())[0] == "normalized":
        print("Error: Wikipedia Article Not Found")
        print("Sending error message back to client...")
        print()
        socket.send(b"Error: Wikipedia Article Not Found")

    else:
        # create json containing only article title and introduction section content
        cleaned_results = {
            "title": raw_results["query"]["pages"][list(raw_results["query"]["pages"].keys())[0]]["title"],
            "content": raw_results["query"]["pages"][list(raw_results["query"]["pages"].keys())[0]]["extract"]
        }
        cleaned_results = json.dumps(cleaned_results)

        print("Created cleaned results:")
        print(cleaned_results)

        # send results back to client
        print("Sending results back to client...")
        print()
        socket.send(cleaned_results.encode())
