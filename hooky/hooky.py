#
# Hooky.py by L3pu5 Hare.
#   A class for submitting formated events to discord  
# 

# References
# https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html

import json, requests

# Manages a single webhook and contains a post definition
class Hook():
    WebHook = ""
    def __init__(this, webHook="") -> None:
        this.WebHook = webHook
    
    # Posts a JSON message
    # Reference: https://birdie0.github.io/discord-webhooks-guide/discord_webhook.html
    def post(this, message):
        r = requests.post(url=this.WebHook, data=message, headers={"Content-Type": "application/json"})
        print(r.content)