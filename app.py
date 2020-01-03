from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8cOgMVUSY3wPWCLkzwSlEKEU1a/GwLvOYmTI6hQ0kFoRcJ8jyHEY8GeMsPncB+Ch'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        app.logger.debug(old_name)
        if old_name is not None and old_name != form.name.data:
            flash('you have changed you name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


class NameForm(FlaskForm):
    name = StringField('Your name?', validators=[DataRequired()])
    submit = SubmitField('提交')