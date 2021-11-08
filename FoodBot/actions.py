# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted
import requests
import zomatoApi
#
#
class ActionGreet(Action):
	
    def name(self) -> Text:
         return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_how_canIhelp")

        return []         
         
class ActionSearchRestaurant(Action):
	
	def name(self)-> Text:
		return "action_search_restaurant"

	def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:     	
        
         city = tracker.get_slot('location')
         cuisine_slot= tracker.get_slot('cuisine')
         print(city)
         print(cuisine_slot)
         
         locationEntity = city
         cuisine =next(tracker.get_latest_entity_values("cuisine"),None)
         print(locationEntity)
         if(locationEntity):
             locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
             print(locationEntities)
             if(locationEntities["restaurants_available"]=="no"):
                 dispatcher.utter_message("Sorry I couldn't find any restaurants  😓")
                 return []
             entity_id=locationEntities["entity_id"]
             entity_type=locationEntities["entity_type"]
             city_id=locationEntities["city_id"]
             SlotSet("location", locationEntities["title"])

        ##get the cuisine id for the cuisine name user provided
         cuisine_id=zomatoApi.getCuisineId(cuisine,city_id)
        
         print("Entities:  ",entity_id," ",entity_type," ",cuisine_id," ",city," ",cuisine)
         print()


         if(cuisine_id==None):
            dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {}".format(cuisine,city))
            return [UserUtteranceReverted()] 
         else:
            ## search the restaurts by calling zomatoApi api
            restaurants=zomatoApi.searchRestaurants(entity_id,entity_type, cuisine_id,"")
            print()
            ## check if restaurants found
            if(len(restaurants)>0):
               
                if(len(restaurants)>5):
                    dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants[:5]})
                    return [SlotSet("more_restaurants", restaurants[5:])]
                else:
                    dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants[:5]})
                    return [SlotSet("more_restaurants", None)]    
            
            else:
                dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {} 😞".format(cuisine,city))
                return [UserUtteranceReverted()] 


class ActionShowMoreRestaurants(Action):
    """
    Show more results of the restaurants
    """
    def name(self) -> Text:
        return "action_show_more_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        restaurants = tracker.get_slot("more_restaurants")
        if restaurants!=None:
            dispatcher.utter_message(text="Here are few more restaurants",json_message={"payload":"cardsCarousel","data":restaurants})
            return [SlotSet("more_restaurants", None)] 
        else:
            dispatcher.utter_message(text="Sorry No more restaurants found")
            return []