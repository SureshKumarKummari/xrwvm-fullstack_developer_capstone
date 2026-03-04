# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
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

    data = {"userName": username}

    if user is not None:

        login(request, user)

        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


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

    context = {}

    # Load JSON data from request body
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:

        # Check if username already exists
        User.objects.get(username=username)

        username_exist = True

    except:

        logger.debug("{} is new user".format(username))

    # If user does not exist
    if not username_exist:

        # Create new user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Login the user
        login(request, user)

        data = {"userName": username, "status": "Authenticated"}

        return JsonResponse(data)

    else:

        data = {"userName": username, "error": "Already Registered"}

        return JsonResponse(data)
