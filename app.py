from flask import Flask
from routes import init_routes
import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

init_routes(app)

if __name__ == "__main__":
    app.run(port=8000, debug=True)