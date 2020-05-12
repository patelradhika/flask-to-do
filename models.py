"""
-------------------------------- Import -------------------------------
"""
from .app import db


"""
-------------------------------- Table --------------------------------
"""
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, nullable=False)
    completed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, task, done):
        self.task = task
        self.done = done

    def __repr__(self):
        return self.task