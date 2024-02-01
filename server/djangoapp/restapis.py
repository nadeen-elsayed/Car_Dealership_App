import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


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
                                   st=dealer["st"], zip=dealer["zip"], state=dealer['state'])
            results.append(dealer_obj)

    return results
# Gets a single dealer from the Cloudant DB with the Cloud Function get-dealerships
# Requires the dealer_id parameter with only a single value
def get_dealer_by_id(dealer_id):
    # Call get_request with the dealer_id param
    URL = "https://apikey-v2-wztwzl2vqrjtynwzpmouki5qaykydaz5iygtyhkx3ht:40233ff7312d84b62b2a9ecc6e2b6496@b3da0739-66b0-434d-ac4e-a114108f111e-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/"
    result = get_request(URL+'_all_docs')
    rows = result['rows']
    the_dealers = 0
    ids = []
    for i in range(5):
        ids.append(rows[i]['id'])
    for i in range(5):
        id = ids[i]
        dealer = get_request(URL+id)
        
        
        if dealer['id'] == dealer_id:
            the_dealer = dealer

    # Create a CarDealer object from response
    dealer_obj = CarDealer(address=the_dealer["address"], city=the_dealer["city"], full_name=the_dealer["full_name"],
                           id=the_dealer["id"], lat=the_dealer["lat"], long=the_dealer["long"],
                           short_name=the_dealer["short_name"],
                           st=the_dealer["st"],  zip=the_dealer["zip"], state=the_dealer['state'])

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
def get_dealer_reviews_from_cf(dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    reviews = get_reviews_json_data(dealer_id)

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
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(f"sentiment: {review_obj.sentiment}")

            # Saving the review object to the list of results
            results.append(review_obj)

    return results
# Function for making HTTP POST requests
def post_request( json_payload, **kwargs):
    
    url = "https://apikey-v2-wztwzl2vqrjtynwzpmouki5qaykydaz5iygtyhkx3ht:40233ff7312d84b62b2a9ecc6e2b6496@b3da0739-66b0-434d-ac4e-a114108f111e-bluemix.cloudantnosqldb.appdomain.cloud/reviews/"

    print(f"POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("An error occurred while making POST request. ")
    status_code = response.status_code
    print(f"With status {status_code}")

    return response

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

# Calls the Watson NLU API and analyses the sentiment of a review
def analyze_review_sentiments(review_text):
    # Watson NLU configuration
   
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f3d28784-79fe-4423-8d8b-6974597e12fa'
    api_key = 'Obq_h-i3IY_sbIc2wC5S1HUmVglIxUalBVehMh0pn4yJ'
    

    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # get sentiment of the review
    try:
        response = nlu.analyze(text=review_text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))
        # sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"

    # print(sentiment_score)
    print(sentiment_label)

    return sentiment_label