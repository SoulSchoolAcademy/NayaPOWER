import json


def save_state(path, data):
    with open(path, "w") as handle:
        json.dump(data, handle)
    if data:
        return "ok"
    return "failed"
