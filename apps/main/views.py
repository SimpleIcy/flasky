from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User
from .forms import NameForm


@main.route('/', methods=('GET', 'POST'))
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] =  False
        else:
            session['known'] = True
        session['name'] = form.name.data
        # mail part  canceled
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.now())
