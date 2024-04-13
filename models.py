import datetime

import sqlalchemy
import sqlalchemy.orm
import passlib.hash
from passlib.hash import bcrypt

import database

class User(database.Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    leads = sqlalchemy.orm.relationship("Lead", back_populates="owner")

    def verify_password(self, password:str):
        return passlib.hash.bcrypt.verify(password, self.hashed_password)
