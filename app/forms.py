from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, ValidationError
from models import Users


class SignUpForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmPass = PasswordField(
        'Confirm Password', validators=[DataRequired()])

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered!")

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError("Email has been used!")


class CreateRecipeForm(FlaskForm):
    class Meta:
        csrf = False
    title = StringField('Title', validators=[InputRequired()])
    instructions = StringField('Instructions', validators=[InputRequired()])
    ingredient = StringField('Ingredient', validators=[InputRequired()])
