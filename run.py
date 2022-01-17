from app import app 
from flask import render_template
from flask_login import login_required

@app.route('/')
@login_required
def index():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)

