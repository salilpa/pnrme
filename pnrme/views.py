from . import app, db
from .forms import *
from .functions import *

from flask import render_template

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
                #do prediction
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
        schedule = get_train_schedule_from_db(train, db["train_schedule"])
        if schedule is None:
            schedule = get_train_schedule_from_server(train)
        if schedule:
            return render_template(
                'schedule.html',
                train_schedule_form=train_schedule_form,
                schedule=schedule
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