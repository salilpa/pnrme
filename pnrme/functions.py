from pnrapi import pnrapi, train_schedule as ts
import re
from datetime import datetime


def pnr_status_check(pnr_number, retries=3):
    """
    get the latest pnr status using pnrapi
    """
    pnr_status = pnrapi.PnrApi(pnr_number)
    if pnr_status.request():
        result = pnr_status.get_json()
        result['status'] = "Success"
        return result
    else:
        result = {
            "pnr": pnr_number
        }
        if pnr_status.error in ["Wrong PNR", "Circular Journey", "Train cancelled"]:
            result['status'] = "Permanent Error"
            result['error'] = pnr_status.error
            return result
        else:
            result['status'] = "Temporary Error"
            result['error'] = pnr_status.error
            if retries > 0:
                return pnr_status_check(pnr_number, retries-1)
            else:
                return result

def get_wl_number(wlValue):
    """
    get the waiting list number from current status
    """
    if not isinstance(wlValue, str) and not isinstance(wlValue, unicode):
        return ""
    wl_re = re.compile("W/L ([\d]*)$")
    if wl_re.findall(wlValue):
        return int(wl_re.findall(wlValue)[0])
    else:
        return ""

def get_prediction(array_conditions, hours_before, wl):
    """
    predict from the given conditions, hours_before and wl, probability of getting a confirmed ticket
    """
    return False


def get_train_schedule(train_number, train_schedule_db):
    """
    check first in database, if not available use train search api to get train schedule
    """
    train_schedule = get_train_schedule_from_db(train_number, train_schedule_db)
    if not train_schedule:
        train_schedule = get_train_schedule_from_server(train_number)
    return train_schedule


def get_boarding_time(boarding_date, boarding_point, train_schedule):
    """
    get boarding train time from schedule, boarding point and schedule
    loop through stations and use it to create exact time
    """
    boarding_month = boarding_date.month
    boarding_day = boarding_date.day
    boarding_year = boarding_date.year
    if train_schedule:
        arrival_time = ""
        for station in train_schedule['schedule']:
            if station['station code'] == boarding_point:
                arrival_time = station['arrival time']
                if arrival_time == "Source":
                    arrival_time = station['departure time']
                break
        if arrival_time:
            boarding_hour = int(arrival_time.split(':')[0])
            boarding_minute = int(arrival_time.split(':')[1])
            time = datetime(boarding_year, boarding_month, boarding_day, boarding_hour, boarding_minute)
            return time
        else:
            return None
    else:
        return None


def get_train_schedule_from_db(train_number, train_schedule_db):
    """
    get the train schedule saved in the db
    """
    train_schedule = train_schedule_db.find_one({'train_number': train_number})
    if train_schedule:
        train_schedule["return_type"] = "schedule"
    return train_schedule


def get_train_schedule_from_server(train_number):
    """
    get train schedule from the server
    """
    train = ts.TrainSearch(train_number)
    if train.request():
        return train.get_json()
    else:
        return None