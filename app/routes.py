from app import app
from flask import render_template, flash, redirect, url_for, request, Flask
from app.forms import LoginForm, RegistrationForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
from app import copygenerator
from flask_mail import Mail, Message

mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'writej.com@gmail.com'
app.config['MAIL_PASSWORD'] = 'pwrjoyrkyostjzvv'
mail.init_app(app)

#@app.route('/')
@app.route('/index_log')
@login_required
def index_log():
    return render_template('index_log.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('content_generator'))#redirect to content_generator!!!!!!!!!!!!
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        #return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/copy_generator', methods=["GET", "POST"])
def copy_generator():

    if request.method == 'POST':
        if 'form1' in request.form:
            prompt = request.form['blogTopic']
            blogT = copygenerator.generateCopyTitle(prompt)
            blogTopicIdeas = blogT
            blogC = copygenerator.generateCopyText(prompt)
            blogCopyText = blogC
        


    return render_template('copy_generator.html', **locals())


@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are mandatory!')
            return render_template('contact.html', form = form)
        else:
            msg = Message(form.subject.data, sender = 'contact@example.com', recipients=['writej.com@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
        """%(form.name.data, form.email.data, form.mesage.data)
            mail.send(msg) 
            return render_template('contact.html', success=True)
    elif request.method == 'GET':
      return render_template('contact.html', form = form)



