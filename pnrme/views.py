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