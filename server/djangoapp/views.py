from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import logging

from .models import CarMake, CarModel
from .restapis import get_request, post_review

logger = logging.getLogger(__name__)


# -----------------------------
# LOGIN VIEW
# -----------------------------
@csrf_exempt
def login_user(request):

    data = json.loads(request.body)

    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    response = {"userName": username}

    if user is not None:
        login(request, user)
        response = {"userName": username, "status": "Authenticated"}

    return JsonResponse(response)


# -----------------------------
# LOGOUT VIEW
# -----------------------------
@csrf_exempt
def logout_request(request):

    logout(request)

    data = {"userName": ""}

    return JsonResponse(data)


# -----------------------------
# REGISTRATION VIEW
# -----------------------------
@csrf_exempt
def registration(request):

    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        user = User.objects.get(username=username)

        return JsonResponse({"userName": username, "error": "Already Registered"})

    except:

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)

        return JsonResponse({"userName": username})


# -----------------------------
# GET DEALERSHIPS
# -----------------------------
def get_dealerships(request):

    url = "http://127.0.0.1:3030/api/dealership"

    dealerships = get_request(url)

    context = {"dealerships": dealerships}

    return JsonResponse(context)


# -----------------------------
# DEALER REVIEWS
# -----------------------------
def get_dealer_reviews(request, dealer_id):

    url = "http://127.0.0.1:3030/api/reviews"

    reviews = get_request(url, dealerId=dealer_id)

    context = {"reviews": reviews}

    return JsonResponse(context)


# -----------------------------
# DEALER DETAILS
# -----------------------------
def get_dealer_details(request, dealer_id):

    url = "http://127.0.0.1:3030/api/dealership"

    dealership = get_request(url, id=dealer_id)

    return JsonResponse({"dealer": dealership})


# -----------------------------
# ADD REVIEW
# -----------------------------
@csrf_exempt
def add_review(request):

    if request.method == "POST":

        data = json.loads(request.body)

        review = {}

        review["name"] = data["name"]
        review["dealership"] = data["dealership"]
        review["review"] = data["review"]
        review["purchase"] = data["purchase"]

        if data["purchase"]:

            review["purchase_date"] = data["purchase_date"]
            review["car_make"] = data["car_make"]
            review["car_model"] = data["car_model"]
            review["car_year"] = data["car_year"]

        review["review_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = post_review(review)

        return JsonResponse(response)
