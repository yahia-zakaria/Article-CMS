from flask import Flask, session
from flask_login import LoginManager, login_manager
from flask_login.utils import login_user
from azure.storage.blob import BlobServiceClient
import pyodbc 
from flask_session import Session
import logging

#creating an app object
app = Flask(__name__, template_folder="../templates", static_folder="../static")

#setting the logging

wsgi_app = app.wsgi_app
app.logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
app.logger.addHandler(streamHandler)

#configuring sessions
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#configuring the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account.login'

#setting the app secret key
app.config["SECRET_KEY"] = "YAHIAZAKARIAEDRISSYAGOUB" 

#database configuration
db_host = 'az-204-srvr.database.windows.net'
db_name = 'Article'
db_user = 'yahia'
db_password = '36RR45ey@@'
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
conn = pyodbc.connect(connection_string)

#storage account and blob config
storage_account = 'azstorageaccountaz204'
blob_container = 'images'
storage_account_key = 'xyOIYbTDRqIehevycQIO3s+rHUTogkFOh2U3MS8Oap23N+fZaMWtmXefF5mLJQa2RU2JtTdJUG6QTiVGkfZVTA=='
storage_url = "https://{}.blob.core.windows.net/".format(storage_account)
blob_service = BlobServiceClient(account_url=storage_url, credential=storage_account_key)
blob_url = f"https://{storage_account}.blob.core.windows.net/{blob_container}/"

#registering blueprints
from app.posts.views import posts_blueprint
from app.account.views import account_blueprint

app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(account_blueprint, url_prefix="/account")


#loading the user data
from models import User
@login_manager.user_loader
def load_user(id):
    if id == "0":
        user = User(email= session["user-email"], password=session["user-password"], id = 0)
        return user
    return User.get_user_by_id(id)