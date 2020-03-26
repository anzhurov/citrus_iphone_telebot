from datetime import datetime

TIME_FORMAT_24_H = '%H:%M'


def is_valid_time(time: str):
    try:
        datetime.strptime(time, TIME_FORMAT_24_H)
        return True
    except ValueError:
        return False
