from slack_sdk import WebClient
from datetime import datetime
import os
import textwrap

# Get Slack Bot Token from environment variables (set in GitHub Secrets)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "#xi-brand-squad"  # Change to your channel
# CHANNEL_ID = "#test-xi-slackbot"  # test channel

# Define the on-call rotation
on_call_rotation = [
    {"name": "David", "slack_id": "@dhaecker"},
    {"name": "Joan", "slack_id": "@johe"},
    {"name": "Kieu", "slack_id": "@kphan"},
    {"name": "Kristen", "slack_id": "@hiserote"},
    {"name": "Maksym", "slack_id": "@maposov"},
    {"name": "Meghanath", "slack_id": "@yadagiri"},
    {"name": "Nirmal", "slack_id": "@nchidambaram"},
    {"name": "Priyam", "slack_id": "@ptejaswin"},
    {"name": "Illia", "slack_id": "@igrybkov"},
    {"name": "Shradha", "slack_id": "@shradagr"},
    {"name": "Aashai", "slack_id": "@aavadhan"},
    {"name": "Raghav", "slack_id": "@raghavk"},
    {"name": "Vahid", "slack_id": "@vazizi"},
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

    message = textwrap.dedent(f"""
    *Weekly Monitoring Owner Alert!*
    This week's owner of UBS backend alerts: {on_call['name']} ({on_call['slack_id']}).

    📣 Nightly Build Triage Instructions
    Every day, please follow this checklist to stay on top of nightly failures:

    🔍 1. Monitor for Failures
    - Check for nightly build failure emails
    - Watch for alerts in #gsp-brand-cicd-alerts Slack channel

    🧪 2. Investigate All Failing Tests
    - Review all failed test cases
    - Identify the root cause for each failure

    🛠️ 3. Take Action Based on Root Cause

    ✅ Test Issue?
    - Fix the test
    - Create a PR with the fix

    🐞 Bug in Brand Service?
    - File a bug in the appropriate tracking system
    - Inform the team via #xi-brand-squad or in standup

    🌐 External Bug?
    - Ensure a bug is filed with the owning team
    - Escalate as needed if there’s no response or impact is critical

    📆 Please make sure this is done every morning after the nightly runs complete. Consistency keeps the pipeline green! ✅
    """)

    response = client.chat_postMessage(channel=CHANNEL_ID, text=message)
    print(f"Message sent: {response['ok']} (On-call: {on_call['name']})")

if __name__ == "__main__":
    send_on_call_alert()
