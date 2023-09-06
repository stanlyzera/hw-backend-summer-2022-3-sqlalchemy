from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Answer:
    title: str
    is_correct: bool

    @classmethod
    def dict_converter(cls, dic: dict):
        return cls(title=dic["title"], is_correct=dic["is_correct"])


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list[Answer] = field(default_factory=list)


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    theme_id = Column(ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
    answers = relationship("AnswerModel", back_populates="question")


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    question = relationship("QuestionModel", back_populates="answers")
