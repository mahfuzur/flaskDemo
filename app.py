from flask import Flask, jsonify
from dotenv import load_dotenv
from sqlalchemy import text

from app.config.db import configure_database, db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# init db
configure_database(app)


def execute_raw_query(query):
    with db.engine.connect() as connection:
        statement = text(query)
        result = connection.execute(statement)
        return result.fetchall()


@app.route("/")
def hello_world():
    q = 'SELECT 10+10'
    results = execute_raw_query(q)

    print(results)
    return '<p>Hello, flaskDemo!</p>'


if __name__ == '__main__':
    app.run()
