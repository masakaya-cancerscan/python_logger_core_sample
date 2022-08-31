import json


def out(message):
    data = json.loads(message)
    json_message = json.dumps(data, indent=2)
    print(json_message)
    return json_message
