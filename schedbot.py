#
# SchedBot `by L3pu5 Hare.
#   This is a python service that posts to a webhook during an event.
#


import sys, getopt, dotenv, os
import time
from collections.abc import MutableSequence
from datetime import datetime
from datetime import timedelta
# Hooky
from hooky import hooky
# Schedule
from schedule import schedule

WEBHOOKS: MutableSequence[hooky.Hook] = []
SCHEDULE: schedule.Schedule

# Post a hello world message
def helloWorld():
    global WEBHOOKS
    for hook in WEBHOOKS:
        print("OK")
        hook.post('''{"embeds": 
                  [
                  {"title": "Hello", "description": "World!", "color":9945513},
                  {"title": "Hello2", "description": "World2!"}
                  ]
                  }''')
    

# cli Args
def handle_commandLineArguments():
    # Globals
    global SCHEDULE  
    global WEBHOOKS  
    #Options
    options = "s:w:e"
    longOptions = ["schedule-file=", "webhook=", "envhook="]
    args, vals = getopt.getopt(args=sys.argv[1:], shortopts=options, longopts=longOptions)
    for thisArg, thisValue in args:
        print(f"ARG: {thisArg}")
        # SCHEDULE
        if thisArg in ("-s", "--schedule-file"):
            SCHEDULE = schedule.Schedule()
            SCHEDULE.load_from_file(thisValue)
            print(SCHEDULE.events[0].toString())
        # WEBHOOK
        if thisArg in ("-w", "--webhook"):
            WEBHOOKS.append(hooky.Hook(thisValue))
        # WEBHOOK FROM DOTENV OR ENV
        if thisArg in ("-e", "--envhook"):
            print("ENTERING")
            dotenv.load_dotenv("./env")
            thisHook = ""
            thisHook = os.environ.get("TESTWEEBHOK")
            print(thisHook)
            if thisHook != "":
                WEBHOOKS.append(hooky.Hook(thisHook))
            thisHook = os.environ.get("WEBHOOK")
            if thisHook != "":
                WEBHOOKS.append(hooky.Hook(thisHook))

    # TODO: FAIL if no SCHEDULE OR WEBHOOK

# Serve the events
def serve_events(now: datetime):
    global SCHEDULE
    global WEBHOOKS
    span = timedelta(minutes=40)
    msg = ""
    for event in SCHEDULE.events:
        if (now + span) > event.time and event.time > now:
            if msg == "":
                msg = '{"embeds":['
            msg += event.toString()
            msg += ","

    if msg != "":
        msg = msg[:-1]
        msg += "]}"
        print(msg)
        for hook in WEBHOOKS:
            print(f"HOOK: {hook}")
            hook.post(msg)  

# Main function loop
def serve():
    # Check time
    now = datetime.now()
    # Check if time is a multiple of 30 or 00
    if( now.minute == 30 or now.minute == 0):
        serve_events(now)
        time.sleep(60*25)
    else:
        time.sleep(55)

# Entry
def main():
    handle_commandLineArguments()
    #serve_events(datetime.fromtimestamp(1726984800-20))
    #helloWorld()
    serve()
    

# Invoke main()
if __name__ == "__main__":
    main()