import requests
import json
import os
import time
import random
# https://jems3.sbc.org.br/api/core/auth/login/
def login(username, password):
    url = "https://jems3.sbc.org.br/api/core/auth/login/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# https://jems3.sbc.org.br/api/core/event/all/?show=active
def get_events(token):
    url = "https://jems3.sbc.org.br/api/core/event/all/?show=active"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
#https://jems3.sbc.org.br/api/core/event/153/
def get_event(token, event_id):
    url = f"https://jems3.sbc.org.br/api/core/event/{event_id}/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
if __name__ == "__main__":
    
    if os.path.isfile("data/jems_token.json"):
        with open("data/jems_token.json", "r") as file:
            json_data = json.load(file)
        print("Token loaded from jems_token.json")
        
    else:        
        username = os.getenv("JEMS_EMAIL")
        password = os.getenv("JEMS_PASSWORD")
        
        if not username or not password:
            print("Erro: As variáveis de ambiente JEMS_EMAIL e JEMS_PASSWORD precisam ser definidas.")
            exit(1)
        
        json_data = login(username, password)
        json.dump(json_data, open("data/jems_token.json", "w"), indent=4)    
        
        
        print("Token saved to jems_token.json")
    
    if not json_data:
        exit(1)
    print(json_data)
    token = json_data["data"]["access"] 
    events = get_events(token)
    json.dump(events, open("data/events.json", "w"), indent=4)
    
    events_details = []
    
    for event in events["data"]:
        time.sleep(random.randint(5, 15))
        get_event_data = get_event(token, event["id"])
        events_details.append(get_event_data)
        json.dump(events_details, open(f"data/event_details.json", "w"), indent=4)
        
        print(f"Event: {event['name']}")
        print(f"ID: {event['id']}")
        print(f"acronym: {event['acronym']}")

        print()
        