import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Function to get dealership data
def get_json_data():
    URL = "https://apikey-v2-wztwzl2vqrjtynwzpmouki5qaykydaz5iygtyhkx3ht:40233ff7312d84b62b2a9ecc6e2b6496@b3da0739-66b0-434d-ac4e-a114108f111e-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/"
    result = get_request(URL+'_all_docs')
    rows = result['rows']

    dealers = []
    ids = []
    for i in range(5):
        ids.append(rows[i]['id'])
    for i in range(5):
        id = ids[i]
        dealer = get_request(URL+id)
        dealers.append(dealer)

    return dealers

# Function to get review data

def get_reviews_json_data(rev_id):
    URL = "https://apikey-v2-wztwzl2vqrjtynwzpmouki5qaykydaz5iygtyhkx3ht:40233ff7312d84b62b2a9ecc6e2b6496@b3da0739-66b0-434d-ac4e-a114108f111e-bluemix.cloudantnosqldb.appdomain.cloud/reviews/"
    result = get_request(URL+'_all_docs')
    rows = result['rows']
    dealers = []
    ids = []
    for i in range(5):
        ids.append(rows[i]['id'])
    for i in range(5):
        id = ids[i]
        dealer = get_request(URL+id)
        print(dealer['id'])
        print(dealers)
        if dealer['id'] == rev_id:
            dealers.append(dealer)
    return dealers
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf( **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_json_data()
    if dealers:
        
        for dealer in dealers:
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results
# Gets a single dealer from the Cloudant DB with the Cloud Function get-dealerships
# Requires the dealer_id parameter with only a single value
def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealerId=dealer_id)

    # Create a CarDealer object from response
    dealer = json_result["entries"][0]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], state=dealer["state"], zip=dealer["zip"])

    return dealer_obj


# Gets all dealers in the specified state from the Cloudant DB with the Cloud Function get-dealerships
def get_dealers_by_state(url, state):
    results = []
    # Call get_request with the state param
    json_result = get_request(url, state=state)
    dealers = json_result["body"]["docs"]
    # For each dealer in the response
    for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Gets all dealer reviews for a specified dealer from the Cloudant DB
# Uses the Cloud Function get_reviews
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    reviews = get_review_json_data(dealer_id)

    if reviews:
     
        # For every review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]

            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Creating a review object
                review_obj = DealerReview(dealership=dealership, id=id, name=name, 
                                          purchase=purchase, review=review_content, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, purchase_date=purchase_date
                                          )

            except KeyError:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            #review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            #print(f"sentiment: {review_obj.sentiment}")

            # Saving the review object to the list of results
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



