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

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealerships(request):
    if request.method == "GET":
      
        # Get dealers from the URL
        dealerships = get_dealers_from_cf()
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



