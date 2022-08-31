import json

def output(message):
    data = json.loads(message)
    json_message = json.dumps(data, indent=2)
    return json_message