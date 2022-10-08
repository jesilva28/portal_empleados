from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email,DataRequired

class login_form(FlaskForm):
    user_id = StringField('Identificación:', validators=[DataRequired()])
    user_pwd = PasswordField('Contraseña:', validators=[DataRequired()])
    submit = SubmitField('Submit')