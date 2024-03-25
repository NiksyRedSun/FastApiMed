


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


def seconds_to_minutes_in_nums(seconds):
    minutes = seconds // 60
    if minutes < 10:
        if minutes == 0:
            minutes = '00'
        else:
            minutes = f"0{minutes}"
    seconds = seconds % 60
    if seconds < 10:
        if seconds == 0:
            seconds = '00'
        else:
            seconds = f"0{minutes}"
    return f'{minutes}:{seconds}'
