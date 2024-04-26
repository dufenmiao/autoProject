import requests

url = "https://hooks.slack.com/services/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"

payload = {
    "channel": "#notice",
    "username": "webhookbot",
    "text": "This is posted to #notice and comes from a bot named webhookbot.",
    "icon_emoji": ":ghost:"
}

response = requests.post(url, json=payload)

print(response.text)
