from flask import Flask, jsonify
from dotenv import load_dotenv
from sqlalchemy import text

from app.config.db import configure_database, db
from app.routes import register_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# init db
configure_database(app)

# register routes
register_routes(app)


def execute_raw_query(query):
    with db.engine.connect() as connection:
        statement = text(query)
        result = connection.execute(statement)
        return result.fetchall()


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
