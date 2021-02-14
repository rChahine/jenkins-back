from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import Session

from .database import Base
from .security import (
    check_encryption, generate_auth_token
)


class User(Base):
    """ Model for users """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String, default="U", nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def verify_password(self, password: str) -> bool:
        return check_encryption(password, self.password)

    def get_auth_token(self) -> str:
        return generate_auth_token({'id': self.id, 'role': self.role})

    @staticmethod
    def get_by_credentials(session: Session, login: str, password: str):
        user = (
            session.query(User)
            .filter(User.username == login)
            .one_or_none()
        )

        if user and user.verify_password(password):
            return user

        return None


class Choice(Base):

    """ Model for choices """

    __tablename__ = "choices"

    id = Column(Integer, primary_key=True)
    wording = Column(String, default="", nullable=False)


class UserChoice(Base):

    """ Model for users and choices association """

    __tablename__ = "users_x_choices"

    idUser = Column(Integer, ForeignKey('users.id'), primary_key=True)
    idChoice = Column(Integer, ForeignKey('choices.id'), primary_key=True)
