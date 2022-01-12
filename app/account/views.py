from flask import render_template, request, redirect, flash, request, Blueprint, url_for
from app.account.forms import RegistrationForm, LoginForm
from wtforms import ValidationError
from flask_login import login_user, logout_user, login_required, current_user
from models import User

account_blueprint = Blueprint("account", __name__, template_folder="templates/")

@account_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User.get_user(form.email.data)
        if user != None:
            raise ValidationError("email is exist!!")
        new_user = User(form.email.data, form.password.data)
        new_user.add_user()
        return redirect(url_for('account.login'))
    return render_template('register.html', form=form)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.get_user(form.username.data)
        if user == None:
            raise ValidationError("Invalid username or password")
        
        if User.check_pass_hash(user[2], form.password.data):
            login_user(User(id= user[0], email=user[1], password=form.password.data))
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('posts.get_posts')
            return redirect(next)
        else:
            raise ValidationError("Invalid username or password")

    return render_template('login.html', form=form)

@account_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('account.login'))