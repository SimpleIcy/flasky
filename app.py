from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from datetime import datetime
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8cOgMVUSY3wPWCLkzwSlEKEU1a/GwLvOYmTI6hQ0kFoRcJ8jyHEY8GeMsPncB+Ch'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('GOOGLE_MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('GOOGLE_MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = 'my@qq.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '360478265@qq.com'
app.config['FLASKY_ADMIN'] = 'deng.changchao@yanwei365.com'


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


migrate = Migrate(app, db)





@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        # old_name = session.get('name')
        # app.logger.debug(old_name)
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                # app.logger.debug('Already sent the email!')
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', new_user=user.username)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data= ' '
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


class NameForm(FlaskForm):
    name = StringField('Your name?', validators=[DataRequired()])
    submit = SubmitField('提交')


