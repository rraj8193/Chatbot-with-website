import requests
import json

headers = {'user-key': 'e247089c39d69d9988cb5976badec56c',
           'Accept': 'application/json'}

def getLocationDetailsbyName(location_name):
    data = {'query': location_name}
    url = 'https://developers.zomato.com/api/v2.1/locations'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    print("Came to getLocationDetailsbyName ")
    print()

    if(len(data["location_suggestions"])>0):
        entity_type = data["location_suggestions"][0]["entity_type"]
        entity_id = data["location_suggestions"][0]["entity_id"]
        title = data["location_suggestions"][0]["title"]
        city_id=data["location_suggestions"][0]["city_id"]
        country_id=data["location_suggestions"][0]["country_id"]
        details={"restaurants_available":"yes","entity_type":entity_type,"entity_id":entity_id,"title":title,"city_id":city_id,"country_id":country_id}
        return details
    else:
        return {"restaurants_available":"no"}

def getCuisineId(cuisine_name,city_id):
    data = {'city_id': city_id,'cuisine_name':cuisine_name}
    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    print("data: ",data)
    cuisines=data["cuisines"]
    cuisineID=None
    for cuisine in cuisines:
            if(cuisine_name.lower() == cuisine["cuisine"]["cuisine_name"].lower()):
                return cuisine["cuisine"]["cuisine_id"]
    return cuisineID


def searchRestaurants(entity_id,entity_type, cuisine_id,search_query):
    url = 'https://developers.zomato.com/api/v2.1/search'
    data = {"entity_id": entity_id, "entity_type": entity_type,
            "cuisines": cuisine_id, "count": "10","order":"asc"}
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    restaurants=[]
    if(len(data["restaurants"])<10):
        restoDataLen=len(data["restaurants"])
    else:
        restoDataLen=10

    for i in range(0, restoDataLen):
        item={}
        item["id"]=data["restaurants"][i]["restaurant"]["id"]
        item["name"]=data["restaurants"][i]["restaurant"]["name"]
        item["url"]=data["restaurants"][i]["restaurant"]["url"]
        item["timings"]=data["restaurants"][i]["restaurant"]["timings"]
        item["votes"]=data["restaurants"][i]["restaurant"]["user_rating"]["votes"]
        item["image"]=data["restaurants"][i]["restaurant"]["featured_image"]
        item["cuisines"]=data["restaurants"][i]["restaurant"]["cuisines"]
        item["ratings"]=data["restaurants"][i]["restaurant"]["user_rating"]["aggregate_rating"]
        item["rating_color"]=data["restaurants"][i]["restaurant"]["user_rating"]["rating_color"]
        item["price_range"]=data["restaurants"][i]["restaurant"]["price_range"]
        item["cost"]=data["restaurants"][i]["restaurant"]["average_cost_for_two"]
        item["location"]=data["restaurants"][i]["restaurant"]["location"]["locality_verbose"]
        item["currency"]=data["restaurants"][i]["restaurant"]["currency"]
        item["user_rating_text"]=data["restaurants"][i]["restaurant"]["user_rating"]["rating_text"]
        restaurants.append(item)
    return restaurants