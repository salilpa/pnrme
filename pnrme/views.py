from . import app, db
from .forms import *
from .functions import *

from flask import render_template, send_file, send_from_directory
import os
import re


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status', methods=('GET', 'POST'))
def status():
    status_form = PnrStatusForm()
    if status_form.validate_on_submit():
            pnr = status_form.pnr.data
            pnr_status_result = pnr_status_check(str(pnr))
            return render_template(
                'status.html',
                status_form=status_form,
                pnr_status_result=pnr_status_result
            )
    else:
        return render_template(
            'status.html',
            status_form=status_form
        )


@app.route('/predictor', methods=('GET', 'POST'))
def predictor():
    prediction_form = PnrPredictionForm()
    if prediction_form.validate_on_submit():
        pnr = prediction_form.pnr.data
        pnr_status_result = pnr_status_check(str(pnr))
        if pnr_status_result['status'] == "Success":
            waiting_list = get_wl_number(pnr_status_result['passenger_status'][0]['current_status'])
            if waiting_list:
                #get the boarding time
                schedule = get_train_schedule(pnr_status_result["train_number"], db["train_schedule"])
                boarding_time = get_boarding_time(pnr_status_result["boarding_date"],
                                                  pnr_status_result["boarding_point"], schedule)
                train_number = pnr_status_result['train_number']
                result = []
                train_class = pnr_status_result['class']
                if boarding_time:
                    hours_before = get_hours(boarding_time, datetime.now())
                    for passenger in pnr_status_result['passenger_status']:
                        quota = get_quota_from_pnr(passenger['booking_status'])
                        curr_status = passenger['current_status']
                        wl = get_wl_number(curr_status)
                        if wl:
                            individual_prediction = get_prediction([{'train': train_number}, {'quota': quota},
                                                                    {'class': train_class}], hours_before, wl)
                        else:
                            individual_prediction = {
                                "data": [],
                                "prediction_val": 1,
                                "message": "Your ticket is already confirmed",
                                "probability": 100,
                                "prediction": True
                            }
                        result.append(individual_prediction)
                    return render_template(
                        'prediction.html',
                        prediction_form=prediction_form,
                        pnr_status_result=pnr_status_result,
                        prediction_result=result
                    )
                else:
                    #send an error message saying boarding time could not be fetched
                    return render_template(
                        'prediction.html',
                        prediction_form=prediction_form,
                        pnr_status_result=pnr_status_result
                    )
            else:
                return render_template(
                    'prediction.html',
                    prediction_form=prediction_form,
                    pnr_status_result=pnr_status_result,
                    pnr_prediction_error="Cannot predict charting status as the ticket is already confirmed or in RAC"
                )
        else:
            return render_template(
                'prediction.html',
                prediction_form=prediction_form,
                pnr_status_result=pnr_status_result,
                pnr_prediction_error="Error in fetching pnr status"
            )
    else:
        return render_template(
            'prediction.html',
            prediction_form=prediction_form
        )


@app.route('/trainSchedule/', methods=('GET', 'POST'))
def train_schedule():
    train_schedule_form = TrainScheduleForm()
    if train_schedule_form.validate_on_submit():
        train = train_schedule_form.train.data
        train = re.sub('[^A-Za-z0-9 ]+', '', train)
        train_number = [int(s) for s in train.split() if s.isdigit()]
        search_result = None
        if len(train_number) > 0:
            train_number_db = str(train_number[0])
            search_result = get_train_schedule_from_db(train_number_db, db["train_schedule"])
        if search_result is None:
            search_result = get_train_schedule_from_server(train)
        if search_result:
            return render_template(
                'schedule.html',
                train_schedule_form=train_schedule_form,
                search_result=search_result
            )
        else:
            return render_template(
                'schedule.html',
                train_schedule_form=train_schedule_form,
                schedule_error="could not find the train"
            )
    else:
        return render_template(
            'schedule.html',
            train_schedule_form=train_schedule_form
        )


@app.route('/trainSchedule/train/<string:train_number>')
def train_schedule_static(train_number):
    search_result = None
    if len(train_number) > 0:
        search_result = get_train_schedule(train_number, db["train_schedule"])
    if search_result:
        seo_train_name = None
        if search_result["return_type"] == "schedule":
            seo_train_name = (search_result["train_name"] + " - " + ', '.join(search_result["train_number"])).title()
        return render_template(
            'schedule.html',
            search_result=search_result,
            seo_train_name=seo_train_name
        )
    else:
        return render_template(
            'schedule.html',
            schedule_error="could not find the train"
        )


@app.route('/BingSiteAuth.xml')
def bing():
    return render_template('BingSiteAuth.xml')


@app.route('/pnrme.zip')
def pnrme_app():
    return send_file('static/downloads/pnrme.zip')


@app.route('/google92a69203eccf42a4.html')
def google():
    return render_template('google92a69203eccf42a4.html')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots/robots.txt')