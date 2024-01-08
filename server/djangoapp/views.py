from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request ,analyze_review_sentiments,get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


cURL = "https://lexlu726-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
carDealerURL = f'{cURL}/dealerships/get'

fiveURL = "https://lexlu726-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
reviewsURL = f'{fiveURL}/api/get_reviews'
postReviewURL = f'{fiveURL}/api/post_review'

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
        # url = "https://lexlu726-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(carDealerURL)
        # Concat all dealer's short name
        # dealer_ids = ' '.join([dealer.id for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
        return render(request,"djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {} 
    if request.method == "GET":
        # carDealerURL = "https://lexlu726-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # reviewsURL = "https://lexlu726-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        dealership = get_dealer_by_id_from_cf(carDealerURL,id = dealer_id) 
        reviews = get_dealer_reviews_from_cf(reviewsURL, dealer_id)
        context["dealership"] = dealership
        context["target"] = reviews
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    url = "https://lexlu726-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"

    context = {} 
    dealership = get_dealer_by_id_from_cf(carDealerURL,id = dealer_id) 
    reviews = get_dealer_reviews_from_cf(reviewsURL, dealer_id)
    context["dealership"] = dealership
    context["reviews"] = reviews
    context["dealer_id"] = dealer_id

    if request.method =="GET":
        context["cars"] = CarModel.objects.all()
        return render (request, 'djangoapp/add_review.html', context)
    if request.user.is_authenticated:

        if request.method =="POST":
            print("*****************************************")
            print(request.POST)
            print(request.POST.dict())
            print("*****************************************")
            inputInfo = request.POST.dict()
            review = dict()
            review["id"] = len(reviews) + 1 
            review["name"] = request.user.username
            review["dealership"] = inputInfo['car']
            review["review"] = inputInfo['content']
            if inputInfo['purchasecheck'] == 'on':
                review["purchase"] = "true"
            else:
                review["purchase"] = "false"
            if review["purchase"] == "true":
                review["purchase_date"] = inputInfo['purchasedDate']
                review["car_make"] = inputInfo['purchasedDate']
                review["car_model"] = inputInfo['purchasedDate']
                review["car_year"] = inputInfo['purchasedDate']


            
            review["time"] = datetime.utcnow().isoformat()
            
            

            json_payload = dict()
            json_payload["review"] = review
            print("****************json_payload***********************")
            print(json_payload)
            print("****************json_payload***********************")
            # postResult = post_request(postReviewURL,json_payload , dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            

    
