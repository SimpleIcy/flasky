from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswitch('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/mail/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account.')
    else:
        flash('Your confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
        and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))

    return render_template('auth/unconfirmed.html')
