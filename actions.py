from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests

class ApiAction(Action):
    def name(self) -> Text:
        return "action_paper_search"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        paper_type = tracker.get_slot('paper_type')
        
        response = requests.get('http://dblp.org/search/publ/api?q={}&format=json&h=1'.format(paper_type)).json()
        title = response['result']['hits']['hit'][0]['info']['title']
        authors = response['result']['hits']['hit'][0]['info']['authors']['author'][0]
        link = response['result']['hits']['hit'][0]['info']['url']

        dispatcher.utter_message('I found a paper called {}.'.format(title))
        return [SlotSet("link", link), SlotSet("authors", authors)]