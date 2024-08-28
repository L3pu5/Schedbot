#
# Hooky.py by L3pu5 Hare.
#   A class for a schedule!
# 


from datetime import datetime
from collections.abc import MutableSequence

class Event():
    time: datetime = datetime.now()
    description: str = ""
    location: str = ""
    def __init__(self) -> None:
        pass

    def fromString(fields: list[str]):
        e: Event = Event()
        e.time = datetime.fromtimestamp(int(fields[0].strip()))
        e.description = fields[1].strip()
        e.location = fields[2].strip()
        return e

    # This is a custom field to create a json blob. Override this in your deployment.
    
    def toString(this) -> str:
        # e8dff5 fce1e4 fcf4dd ddedea daeaf6
        # 232223245 16572900 16577757 14544362 14346998
        colourMap = {"Registration Desk": 16776960, "The Park": 16776960, "Main Stage": 5763719, "Games Zone": 3447003, "Side Stage": 15548997, "Dealers Den": 10181046}
        output = "{"
        output += f'"title":"{this.description}", "description":":hotel: {this.location} :watch: {this.time.strftime("%I.%M%p").lower()}"'
        if this.location in colourMap:
            output += f',"color":{colourMap[this.location]}'
        output += "}"
        return output


class Schedule():
    events: MutableSequence[Event] = []

    def __init__(self) -> None:
        pass

    def load_from_file(this, path):
        file = open(path, "r")
        for line in file.readlines():
            fields = line.split('|')
            if(len(fields) != 3):
                continue
            else:
                this.events.append( Event.fromString(fields))
        file.close()
