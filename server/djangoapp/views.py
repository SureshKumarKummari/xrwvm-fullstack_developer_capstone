# Uncomment the required imports before adding the code

import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# ---------------------------------
# GET CARS
# ---------------------------------


def get_cars(request):

    count = CarMake.objects.filter().count()

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:

        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# Get an instance of a logger
logger = logging.getLogger(__name__)


# ---------------------------------
# LOGIN VIEW
# ---------------------------------
@csrf_exempt
def login_user(request):

    data = json.loads(request.body)

    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    data = {"userName": username}

    if user is not None:

        login(request, user)

        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


# ---------------------------------
# LOGOUT VIEW
# ---------------------------------
@csrf_exempt
def logout_request(request):

    logout(request)

    data = {"userName": ""}

    return JsonResponse(data)


# ---------------------------------
# REGISTRATION VIEW
# ---------------------------------
@csrf_exempt
def registration(request):

    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:

        User.objects.get(username=username)

        username_exist = True

    except User.DoesNotExist:

        logger.debug("{} is new user".format(username))

    if not username_exist:

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        login(request, user)

        data = {"userName": username, "status": "Authenticated"}

        return JsonResponse(data)

    else:

        data = {"userName": username, "error": "Already Registered"}

        return JsonResponse(data)


# ---------------------------------
# GET DEALERSHIPS
# ---------------------------------
def get_dealerships(request, state="All"):

    if state == "All":

        endpoint = "/fetchDealers"

    else:

        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


# ---------------------------------
# GET DEALER DETAILS
# ---------------------------------
def get_dealer_details(request, dealer_id):

    if dealer_id:

        endpoint = "/fetchDealer/" + str(dealer_id)

        dealership = get_request(endpoint)

        return JsonResponse({
            "status": 200,
            "dealer": dealership
        })

    else:

        return JsonResponse({
            "status": 400,
            "message": "Bad Request"
        })


# ---------------------------------
# GET DEALER REVIEWS
# ---------------------------------
def get_dealer_reviews(request, dealer_id):

    if dealer_id:

        endpoint = "/fetchReviews/dealer/" + str(dealer_id)

        reviews = get_request(endpoint)

        if not isinstance(reviews, list):
            logger.warning("Unexpected reviews payload: %r", reviews)
            reviews = []

        for review_detail in reviews:
            try:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                review_detail['sentiment'] = response.get('sentiment', 'neutral')
            except Exception as err:
                logger.exception("Error analyzing sentiment: %s", err)
                review_detail['sentiment'] = 'neutral'

        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })

    else:

        return JsonResponse({
            "status": 400,
            "message": "Bad Request"
        })

@csrf_exempt
def add_review(request):

    if not request.user.is_anonymous:

        data = json.loads(request.body)

        try:
            response = post_review(data)
            print(response)

            return JsonResponse({"status": 200})

        except Exception as err:
            logger.exception("Error posting review: %s", err)

            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })

    else:

        return JsonResponse({
            "status": 403,
            "message": "Unauthorized"
        })
