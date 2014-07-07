from flask_wtf import Form
from wtforms import ValidationError, SubmitField, IntegerField
from wtforms.validators import Required


class PnrStatusForm(Form):
    pnr = IntegerField('pnr number',
                       description='10 digit pnr number',
                       validators=[Required(message='required field')])
    submit_button = SubmitField('check pnr status')

    def validate_pnr(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError('pnr number should be of 10 digits')