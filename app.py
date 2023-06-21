from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import text

from app.config.db import configure_database, db
from app.config.jwt import initialize_jwt
from app.routes import register_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# init services
configure_database(app)
initialize_jwt(app)

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
