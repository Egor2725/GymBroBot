

def extract_weight_and_times_from_message(msg):
    try:
        weight, times = msg.replace('/add_set', '').split()
    except ValueError as err:
        return None, None

    return weight, times
