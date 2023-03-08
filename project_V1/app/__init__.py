from flask import Flask
from flask_bcrypt import Bcrypt
from flask_toastr import Toastr

app = Flask(__name__)

app.secret_key = 'mandarinas'
app.config['TOASTR_POSITION_CLASS'] = 'toast-bottom-right'

bcrypt = Bcrypt(app)
toastr = Toastr(app)
