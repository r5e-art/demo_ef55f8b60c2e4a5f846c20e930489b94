from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    items = relationship("Item", back_populates="user")


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="items")
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
