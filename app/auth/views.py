from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from ..email import send_email
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # 这个判断条件，用于判断未确认前
        if not current_user.confirmed and request.endpoint and request.endpoint != 'static' and request.blueprint != 'auth':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/auth/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('This email has not been registered yet.')
            return redirect(url_for('auth.register'))
        else:
            token = user.generate_reset_token()
            send_email(user.email,
                       'Reset Your Password',
                       'auth/email/reset_password',
                       user=user,
                       token=token)
            flash(
                'An email with instructions to reset your password has been sent to your email.'
            )
            return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)


@auth.route('/auth/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('The reset link is invalid or has expired.')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/auth/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has benn updated.')
            redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 这个函数会在会话中把该用户标记未已登录
            login_user(user, form.remember_me.data)
            # 用户访问未授权的URL时会显示登录表单，flask_login会把源地址保存在next参数中，登录后返回这个界面
            # 如果直接登录则回到首页
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/auth/logout')
# 确保当前用户登录并授权
@login_required
def logout():
    # 退出当前用户
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        # 要记得commit
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,
                   'Confirm Your Account',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('A confirmation email has been sent to your email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/auth/confirm/<token>')
# 这个修饰器保证点击确认邮件中的链接后，要先登录，才能执行这个视图函数
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.index'))


@auth.route('/auth/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/auth/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Confirm Your Account',
               'auth/email/confirm',
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))