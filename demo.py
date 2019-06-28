# encoding:utf-8
from datetime import datetime, timedelta


def get_day_zero_time(date):
    result = datetime.now().replace(year=date.year, month=date.month,
                                    day=date.day, hour=0, minute=0, second=0)
    return result


today = datetime.now()
zero_time = get_day_zero_time(today)

start = zero_time - timedelta(days=zero_time.weekday())
end = start + timedelta(days=6)