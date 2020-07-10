from flask import Flask, request, make_response
import slack 
from slack import WebClient
from slack.errors import SlackApiError
import json
import requests
import os
from dotenv import load_dotenv


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    

# Load environment variables
load_dotenv('.env')

app = Flask(__name__)

general_channel = os.getenv('GENERAL_CHANNEL')
introductions_channel = os.getenv('INTRODUCTIONS_CHANNEL')
random_channel = os.getenv('RANDOM_CHANNEL')
test_bot_channel = os.getenv('TEST_BOT_CHANNEL')


slack_token = os.getenv('SLACK_API_TOKEN')
slack_client = WebClient(token = slack_token)

@app.route('/', methods=['GET', 'POST'])
def check():
        
    if request.method == 'GET':
        return make_response("These are not the slackbots you're looking for.", 404)
    else:
        events_data = json.loads(request.data.decode('utf-8'))

        if 'challenge' in events_data:
            return make_response(
                events_data.get('challenge'), 200, {'content_type': 'application/json'}
            )

        if "event" in events_data:
            event_type = events_data["event"]["type"]

            if event_type == "app_mention":
                text = events_data["event"]["text"].lower()
                user_id = events_data["event"]["user"]
                if "hi" in text:
                    notify_slack("Hi <@" + user_id + ">, what can I do for you? Type\n*channel topic* to see topic for this channel\n*gsoc website* to get link to Google Summer of Code website\n*updates* to get GSoC related updates")
                elif "channel topic" in text:
                    notify_slack("This channel is to help aspiring GSoC students get accepted into the program. If you are not a GSoC veteran(i.e you are here to get help on getting into gsoc) introduce yourself ( 2 Names and Profile picture) so we get to know you.")
                elif "gsoc website" in text:
                    notify_slack("Google Summer of Code official website https://summerofcode.withgoogle.com/")
                elif "updates" in text:
                    notify_slack("There isn't any updates for now.")
                elif "timeline" in text:
                    notify_slack(get_timeline())
                else:
                    notify_slack("Hi <@" + user_id + ">, sorry I can't help you with that. Type\n*channel topic* to see topic for this channel\n*gsoc website* to get link to Google Summer of Code website\n*updates* to get GSoC related updates\n*timeline* to get the current GSoC timeline for this month")
                return make_response("", 200)
            
            if event_type == "team_join":
                user = events_data["event"]["user"]
                welcome_template = "Welcome to Cameroon GSoCers Workspace. \nTell us a little bit about yourself, Your Real Names, Location, \nSpecialty/Department, Your Interests, Any specific questions ? \nLearn Netiquette Rules on http://www.albion.com/netiquette/corerules.html \nLearn How To Ask Smart Questions on http://www.catb.org/esr/faqs/smart-questions.html \nRemember to put your Real Names on your profile and a professional profile picture :) \nTake note of the channel topic and ALL pinned posts"
                notify_slack("Hi <@" + user + "> ," + welcome_template)
                return make_response("", 200)

        return make_response("Not implemented.", 404)


def get_timeline():
    r = requests.get('https://raw.githubusercontent.com/muarachmann/gsoc_timeline_scrapper/master/data.json')
    c = r.content    
    timeline = json.loads(c)
    
    # get the timeline
    return '\n'.join(timeline["data"])

def notify_slack(msg):
    try:
        response = slack_client.chat_postMessage(
            channel=test_bot_channel,
            text=msg
            )
        print("ok")
    except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
