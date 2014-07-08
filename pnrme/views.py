from . import app
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
        waiting_list = get_wl_number(pnr_status_result['current_status'])
        if pnr_status_result['status'] == "Success" and waiting_list:
            x=""
        else:
            return render_template(
                'prediction.html',
                prediction_form=prediction_form,
                pnr_status_result=pnr_status_result,
                pnr_prediction_error = "Cannot predict confirmation status as the ticket is already confirmed or in RAC or there was an error in fetching pnr status"
            )
    else:
        return render_template(
            'prediction.html',
            prediction_form=prediction_form
        )