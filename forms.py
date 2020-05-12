"""
-------------------------------- Import -------------------------------
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


"""
-------------------------------- Forms --------------------------------
"""
class AddTodo(FlaskForm):
    item = StringField(validators=[DataRequired()])
    submit = SubmitField('Add Reminder')
