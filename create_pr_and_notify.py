import requests
import os

# === GitHub Config ===
REPO = "XI/brand-service"
OWNER = "XI"
BASE_BRANCH = "main"
HEAD_BRANCH = "development"
GITHUB_API = "https://git.corp.adobe.com/api/v3"
GITHUB_TOKEN = os.getenv("GH_ENTERPRISE_TOKEN")

# === Slack Config ===
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#xi-brand-squad"

def create_pull_request():
    url = f"{GITHUB_API}/repos/{OWNER}/{REPO}/pulls"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": "🔁 Weekly PR: development → main",
        "head": HEAD_BRANCH,
        "base": BASE_BRANCH,
        "body": "This pull request was created automatically to sync changes from development to main.",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        pr_url = response.json()["html_url"]
        print("✅ PR created:", pr_url)
        return f"✅ Weekly PR created: {pr_url}"
    elif response.status_code == 422 and "A pull request already exists" in response.text:
        print("⚠️ PR already exists")
        return "⚠️ A PR from development to main already exists."
    else:
        print(f"❌ Failed to create PR: {response.status_code} — {response.text}")
        return f"❌ Failed to create PR: {response.status_code}"

def send_slack_message(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL,
        "text": message
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.ok and response.json().get("ok"):
        print("✅ Slack message sent.")
    else:
        print("❌ Failed to send Slack message:", response.text)

if __name__ == "__main__":
    pr_result = create_pull_request()
    send_slack_message(f"📣 *Brand Service Weekly Prod PR Update*\n{pr_result}")
