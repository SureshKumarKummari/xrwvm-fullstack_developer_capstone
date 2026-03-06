# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


# ----------------------------------------
# GET REQUEST TO BACKEND API
# ----------------------------------------
def get_request(endpoint, **kwargs):

    params = ""

    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {}".format(request_url))

    try:
        response = requests.get(request_url)
        return response.json()

    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")


# ----------------------------------------
# SENTIMENT ANALYSIS MICROSERVICE
# ----------------------------------------
def analyze_review_sentiments(text):

    request_url = sentiment_analyzer_url + "analyze/" + quote(text, safe="")

    try:
        response = requests.get(request_url, timeout=5)
        return response.json()

    except (requests.RequestException, ValueError) as err:
        print(f"Sentiment analyzer error: {err}")
        return {"sentiment": "neutral"}


# ----------------------------------------
# POST REVIEW TO BACKEND
# ----------------------------------------
def post_review(data_dict):

    request_url = backend_url + "/insert_review"

    try:
        response = requests.post(request_url, json=data_dict)

        print(response.json())

        return response.json()

    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
