import requests, json
import time
import urllib3

YELLOW_COLOR = '\033[33m'
CEND = '\033[0m'
CBOLD = '\033[1m'
GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'

# events could be placed here and triggered at will
events = ['team_join', 'app_mention']

myJson = {
        "token": "XXXXXXXXXX",
        "team_id": "XXXXXXXXXX",
        "api_app_id": "XXXXXXXXXX",
        "event": {
                "type": "event",
                "event_ts": str(time.time()),
                "user": "USERID",
                "text": "Hello world"
        },
        "type": "event_callback",
        "authed_users": [
                "USERID"
        ],
        "event_id": "XXXXXXXXXX",
        "event_time": str(time.time())
}

def prepare_json_body(event, userid, text):
    # other parameters could be placed here

    AUTH_USERS = []
    AUTH_USERS.append(user_id)

    myJson['event']['type'] = event
    myJson['event']['text'] = text
    myJson['event']['user'] = userid
    myJson['authed_users'] = AUTH_USERS
    return myJson

def connection_available():
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', 'http://127.0.0.1:5000?q=local')
        if response.status == 202:
            print("Connection to host http://127.0.0.1:5000" + GREEN_COLOR + CBOLD + " OK" + CEND)
            return True
        else:
            return False
    except Exception as e:
        print("Connection to host " + GREEN_COLOR + "http://127.0.0.1:5000" + CEND, end=" ")
        print("refused please ensure it is running by running the " + YELLOW_COLOR + CBOLD + "app.py " + CEND + "file")
        return False

def get_slack_event():
    print("##########################################################\n")
    print("  This program is for testing the slack bot api locally")
    print("  Event triggers could be one of the following")
    print("\t", end="")
    for event in events:
        if event != events[-1]:
            print(YELLOW_COLOR + CBOLD + f"'{event}', " + CEND, end="")
        else:
            print(YELLOW_COLOR + CBOLD + f"'{event}' " + CEND, end="")

    print("\n\n#######################################################\n")

    selected_event = input("Input a test event: ")
    if selected_event not in events:
        print("Please select an event from the available event list")
        exit(0)
    else:
        if selected_event == 'app_mention':
            text = input("Say something to bot: ")
        else:
            text = "Hello world"
        user_id = input("Input an slack user id: ")

    return selected_event, user_id, text

user_event, user_id, user_text = get_slack_event()
jsonObject = prepare_json_body(user_event, user_id, user_text)

# converting dictionary to JSON to parse it in the request
print("\n=========================================")
print("JSON BODY BEING PARSED")
print(GREEN_COLOR + CBOLD + json.dumps(jsonObject, sort_keys=True, indent=3) + CEND)
print("=========================================\n")


if connection_available():
    # creating a post request to server
    json_data = json.dumps(jsonObject, sort_keys=True, indent=3)
    r = requests.post("http://127.0.0.1:5000/", data=json_data)

    if r.status_code == 200:
        print("request successfully made to slack bot -- we could get the return the response here too :)")
    else:
        print(f"request failed {r.text}")

else:
    print("Please make sure the server is running and you have internet connection")