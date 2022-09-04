import json

from cs.core.utils.config import AppConfig


def out(message):
    data = json.loads(message)
    json_message = json.dumps(data, indent=2)
    print(json_message)

    print(AppConfig.get_properties("test"))
    return json_message
