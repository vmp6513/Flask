from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2',
                                         message='Passwords must match.')
                             ])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2',
                                         message='Passwords must match.')
                             ])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(1, 64),
                                    Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(1, 64),
                                    Email()])
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(8, 32),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Username must have only letters, numbers, dots or underscores.'
            )
        ])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2',
                                         message='Passwords must match.')
                             ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # 注意，如果表单类中定义了validate_开头且后面跟着字段名的方法，这个方法就会和常规的验证函数一起使用（使用raise机制）
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            # 用raise报错？
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
