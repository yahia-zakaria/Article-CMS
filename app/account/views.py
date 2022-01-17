from flask import render_template, request, redirect, flash, request, Blueprint, url_for, session
from app.account.forms import RegistrationForm, LoginForm
from wtforms import ValidationError
from flask_login import login_user, logout_user, login_required, current_user
from models import User
import msal
from app.config import Config
import uuid

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
    session["state"] = str(uuid.uuid4())
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

    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    print("##############################################")
    print(auth_url)
    print("##############################################")
    return render_template('login.html', form=form, title='Sign In', auth_url=auth_url)

@account_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('account.login'))


def _save_cache(cache):
  if cache.has_state_changed:
     session['token_cache'] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
     Config.CLIENT_ID, authority=authority or Config.AUTHORITY,
    client_credential=Config.CLIENT_SECRET, token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
    scopes or [],
    state=state or str(uuid.uuid4()),
    redirect_uri=url_for('account.authorized', _external=True, _scheme='https'))

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

@account_blueprint.route(Config.REDIRECT_PATH) # Its absolute URL must match your app's
def authorized():
  if request.args.get('state') != session.get('state'):
   return redirect(url_for('account.login')) # Failed, go back home
  if 'error' in request.args: # Authentication/Authorization failure
    return render_template('auth_error.html', result=request.args)
  if request.args.get('code'):
    cache = _load_cache()
    result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
     request.args['code'],
     scopes=Config.SCOPE,
     redirect_uri=url_for('account.authorized', _external=True, _scheme='https'))
         
    if 'error' in result:
      return render_template('auth_error.html', result=result)
    session['user'] = result.get('id_token_claims')
    user = User(email=result.get("id_token_claims", {}).get("preferred_username"), password=str(uuid.uuid4()), id=str(uuid.uuid4()))
    login_user(user)
    _save_cache(cache)