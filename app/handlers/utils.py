

def extract_weight_and_times_from_message(msg):
    try:
        weight, times = msg.lower().replace('подход ', '').split()
        weight, times = float(weight), int(times)
    except ValueError:
        return None, None

    return weight, times
