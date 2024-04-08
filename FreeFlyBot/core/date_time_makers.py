from datetime import datetime, timedelta
from core import create_log

from settings import (
    POSSIBLE_DATE_FORMATS,
    POSSIBLE_TIME_FORMATS,
    POSSIBLE_HOUR_FORMATS,
    POSSIBLE_MINUT_FORMATS,
)


def str_to_date(date_str: str) -> tuple[str, str, str]:
    for i in POSSIBLE_DATE_FORMATS:
        date_str = date_str.replace(i, ' ')
    date_list = date_str.split(sep=' ')
    return (date_list[0], date_list[1], date_list[2])


def str_to_time(time_str: str) -> tuple[tuple[str, ...], int]:
    for i in POSSIBLE_TIME_FORMATS:
        time_str = time_str.replace(i, ' ')
    main_time_list = []
    minuts_before = 0
    if len(time_str) == 2:
        main_time_list = time_str.split(sep=' ')
    elif len(time_str) > 2:
        main_time_list = time_str.split(sep=' ')[:2]
        adv_time_list = time_str.split(sep=' ')[2:]

        hours = 0
        minuts = 0
        for i in adv_time_list:
            if i[-1] in POSSIBLE_HOUR_FORMATS:
                hours = abs(int(i[:-1]))
            elif i[-1] in POSSIBLE_MINUT_FORMATS:
                minuts = abs(int(i[:-1]))
        minuts_before = hours*60 + minuts
    return tuple(main_time_list), minuts_before


def make_datetime(date_str: str, time_str: str) -> tuple[datetime, datetime]:
    raw_date = str_to_date(date_str)
    raw_time, time_before = str_to_time(time_str)

    try:
        date = datetime.strptime(
            f"{raw_date[0]} {raw_date[1]} {raw_date[2]} {raw_time[0]} {raw_time[1]}",
            f'%Y %m %d %H %M'
        )
        date_adt = None
        if time_before > 0:
            date_adt = date - timedelta(time_before)
        else:
            date_adt = date

        return date, date_adt
    except Exception as err:
        create_log(err, 'error')
        return datetime(2024, 1, 1, 1, 1, 1), datetime(2024, 1, 1, 1, 1, 1) 
