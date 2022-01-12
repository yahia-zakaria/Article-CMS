from flask import Flask
from flask_login import LoginManager, login_manager
from flask_login.utils import login_user
import pypyodbc as pyodbc

app = Flask(__name__, template_folder="../templates", static_folder="../static")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account.login'

app.config["SECRET_KEY"] = "YAHIAZAKARIAEDRISSYAGOUB" 

db_host = 'az-204-srvr.database.windows.net'
db_name = 'Article'
db_user = 'yahia'
db_password = '36RR45ey@@'
connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
conn = pyodbc.connect(connection_string)

from app.posts.views import posts_blueprint
from app.account.views import account_blueprint

app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(account_blueprint, url_prefix="/account")

from models import User
@login_manager.user_loader
def load_user(id):
    return User.get_user_by_id(id)