from flask_login import UserMixin
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'stepsLogger-secret-key'

    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    stepsRecords = db.relationship('Steps', backref='author', lazy=True)


class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps_completed = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    '''
    inserts a new stepRecord into the table Steps.
    Every row has a unique id to identify the specific record.
        EXAMPLE
            stepsRecord = Steps(steps_completed=steps_completed,
                        comment=comment, author=user)
            stepsRecord.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
        delete()
        deletes a stepsRecord from the database
        For this function to work, the stepRecord identified by the id should exist in Steps
        EXAMPLE
            stepsRecord = Steps.query.get_or_404(stepsRecord_id)
            stepsRecord.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an existing stepRecord in the database
        For update to work, the stepRecord identified by the id should exist in Steps
        EXAMPLE
            stepsRecord = Steps.query.filter(Steps.id == id).one_or_none()
            stepsRecord.steps_completed = 8000
            stepsRecord.update()
    '''

    def update(self):
        db.session.commit()
