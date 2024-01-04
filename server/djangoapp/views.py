from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request ,analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
        context = {}
        if request.method == "GET":
            return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
        context = {}
        if request.method == "GET":
            return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return redirect("djangoapp:registration")



# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request): 
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context) 
    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = User.objects.create_user(username=username, password=password)
    #     login(request,user)
    #     return redirect("djangoapp:registration")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {} 
    if request.method == "GET":
        url = "https://lexlu726-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["short_name"] = dealer_names
        return render(request,"djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {} 
    if request.method == "GET":
        url = "https://lexlu726-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, dealer_id)
        print("sdnfoasndfoaienfoaneofaef")
        print(dealerships)
        print("sdnfoasndfoaienfoaneofaef")
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer for dealer in dealerships])
        # Return a list of dealer short name
        # return render(request,"djangoapp/index.html", context)
        return HttpResponse(dealerships)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    url = "https://lexlu726-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
    print("*****************************************")
    print(request.method)
    print("*****************************************")
    if request.user.is_authenticated:

        if request.method =="GET":
            print("************************")
            print(request.user.is_authenticated)
            print("************************")
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = 11
            review["review"] = "This is a great car dealer"
            review["purchase"] = false
            json_payload = dict()
            json_payload["review"] = review
            print("************************")
            print(json_payload)
            print("************************")
            postResult = post_request(url,json_payload , dealerId=dealer_id)
            print("************************")
            print(postResult)
            print("************************")
            return HttpResponse(postResult)
            

    
