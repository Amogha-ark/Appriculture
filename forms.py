from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo,NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Name',
                        validators=[DataRequired()])
    number = StringField('RTC Number', validators=[DataRequired()])
    phoneno = IntegerField('Phone No',validators=[DataRequired()])
    soil = SelectField('Soil Type', choices=[('Red', 'Red'), ('Black', 'Black')]) 
    submit = SubmitField('register')