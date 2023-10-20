from src import app
from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": "*", "methods": "*", "headers": "*"}})

app.run(port=3000)
