


def seconds_to_minutes(seconds):
    if seconds > 60:
        minutes = seconds // 60
        if minutes == 1:
            return "1 минута"
        elif 2 <= minutes <= 4:
            return f"{minutes} минуты"
        else:
            return f"{minutes} минут"
    else:
        return 'меньше минуты'
