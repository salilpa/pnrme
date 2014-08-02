from functions import *
from . import db


def test_pnr_status_check():
    wrong_pnr = pnr_status_check("1234567890", retries=3)
    assert wrong_pnr['status'] == "Permanent Error"


def test_get_wl_number():
    assert get_wl_number(u'RAC 40') == ""
    assert get_wl_number(u'W/L 6') == 6
    assert get_wl_number(u'RS12 15') == ""


def test_get_train_schedule_from_db():
    assert get_train_schedule_from_db("", db["train_schedule"]) is None
    assert get_train_schedule_from_db("00852", db["train_schedule"]) is not None


def test_get_train_schedule_from_server():
    assert get_train_schedule_from_server("9999") is None
    assert get_train_schedule_from_server("11012")["return_type"] == "schedule"
    assert get_train_schedule_from_server("himac")["return_type"] == "train list"


def test_get_train_schedule():
    assert get_train_schedule("", db["train_schedule"]) is None
    assert get_train_schedule("00852", db["train_schedule"]) is not None


def test_get_boarding_time():
    boarding_date = datetime(2020, 11, 16)
    train_schedule = get_train_schedule("16649", db["train_schedule"])
    boarding_time = get_boarding_time(boarding_date, "TCR", train_schedule)
    boarding_time_no_schedule = get_boarding_time(boarding_date, "TCR", None)
    boarding_time_wrong = get_boarding_time(boarding_date, "MAS", train_schedule)
    assert boarding_time == datetime(2020, 11, 16, 11, 52)
    assert boarding_time_wrong is None
    assert boarding_time_no_schedule is None