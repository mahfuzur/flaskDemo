from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def configure_database(app):
    # MySQL configuration values
    db_connection = os.getenv('DB_CONNECTION')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_database = os.getenv('DB_DATABASE')
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')

    # Create the MySQL connection URL
    db_url = f"{db_connection}://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
