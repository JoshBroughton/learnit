from learnit_app import app
from learnit_app.main.routes import main
from learnit_app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)