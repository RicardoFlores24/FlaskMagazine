from app import app

from app.controllers.auth import auth
from app.controllers.magazines import magazines

app.register_blueprint(auth)
app.register_blueprint(magazines)


if __name__=="__main__":
    app.run(debug=True)
