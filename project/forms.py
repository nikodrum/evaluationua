# -*- coding: UTF-8 -*-
from flask import Flask
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class MyForm(Form):
    street = StringField('Улица')
    num_build = StringField('Номер дома')
    year = StringField('Год постройки')
    room = StringField('Количество комнат')
    all_area = StringField('Общая площадь')
    all_floors = StringField('Этажей в доме')
    submit = SubmitField('Посчитать')

class MyForm_result(Form):
    button_for_delete_and_return_to_index = SubmitField('ЕЩЕ')
