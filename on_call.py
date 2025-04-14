from slack_sdk import WebClient
from datetime import datetime
import os

# Get Slack Bot Token from environment variables (set in GitHub Secrets)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "#xi-brand-squad"  # Change to your channel

# Define the on-call rotation
on_call_rotation = [
    {"name": "David", "slack_id": "@dhaecker"},
    {"name": "Illia", "slack_id": "@igrybkov"},
    {"name": "Joan", "slack_id": "@johe"},
    {"name": "Kieu", "slack_id": "@kphan"},
    {"name": "Kristen", "slack_id": "@hiserote"},
    {"name": "Maksym", "slack_id": "@maposov"},
    {"name": "Meghanath", "slack_id": "@yadagiri"},
    {"name": "Nirmal", "slack_id": "@nchidambaram"},
    {"name": "Priyam", "slack_id": "@ptejaswin"},
    {"name": "Shradha", "slack_id": "@shradagr"},
    {"name": "Sriram", "slack_id": "@sravindr"},
]

# Determine who is on-call this week based on ISO week number
def get_on_call_person():
    week_number = datetime.today().isocalendar()[1]
    return on_call_rotation[week_number % len(on_call_rotation)]

# Send message to Slack
def send_on_call_alert():
    if not SLACK_BOT_TOKEN:
        raise ValueError("Missing Slack token!")

    client = WebClient(token=SLACK_BOT_TOKEN)
    on_call = get_on_call_person()
    message = f"🚨 *Weekly Monitoring Owner Alert!* 🚨\nThis week's owner of UBS backend alerts: {on_call['name']}({on_call['slack_id']}).\nPlease monitor all #gsp-brands-alerts and #gsp-brands-alerts-stage messages and create bug reports or escalations to the team, as needed."

    response = client.chat_postMessage(channel=CHANNEL_ID, text=message)
    print(f"Message sent: {response['ok']} (On-call: {on_call['name']})")

if __name__ == "__main__":
    send_on_call_alert()
