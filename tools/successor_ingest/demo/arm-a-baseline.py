def save_state(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)
    return 'ok' if data else 'failed'
