from typing import Optional

from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    AnswerModel,
    Question,
    QuestionModel,
    Theme,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        await self.app.database.orm_add(theme)
        return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        response = await self.app.database.orm_select(query=query)
        theme = response.scalar()
        if theme:
            return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        response = await self.app.database.orm_select(query=query)
        theme = response.scalar()
        if theme:
            return Theme(id=theme.id, title=theme.title)

    async def list_themes(self) -> list[Theme]:
        query = select(ThemeModel)
        response = await self.app.database.orm_select(query=query)
        themes = response.scalars().all()
        return [Theme(title=theme.title, id=theme.id) for theme in themes]

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        query = (
            select(QuestionModel)
            .where(QuestionModel.title == title)
            .options(selectinload(QuestionModel.answers))
        )
        response = await self.app.database.orm_select(query=query)
        question = response.scalar()
        if question:
            return Question(
                id=question.id,
                title=question.title,
                theme_id=question.theme_id,
                answers=[
                    Answer(title=answer.title, is_correct=answer.is_correct)
                    for answer in question.answers
                ],
            )

    async def create_answers(self, answers: list[Answer], question_id: int) -> None:
        answers_db = []
        for answer in answers:
            one_answer_db = AnswerModel(
                title=answer.title,
                is_correct=answer.is_correct,
                question_id=question_id,
            )
            answers_db.append(one_answer_db)
        await self.app.database.orm_add(answers_db)

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        if len(answers) < 2:
            raise HTTPBadRequest
        if sum(1 for answer in answers if answer.is_correct) != 1:
            raise HTTPBadRequest
        question = QuestionModel(title=title, theme_id=theme_id, answers=[])
        await self.app.database.orm_add(question)
        await self.create_answers(answers=answers, question_id=question.id)
        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=answers,
        )

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        query = select(QuestionModel)
        if theme_id:
            if await self.get_theme_by_id(theme_id):
                query = query.where(QuestionModel.theme_id == theme_id)
            else:
                raise HTTPNotFound
        response = await self.app.database.orm_select(
            query=query.options(selectinload(QuestionModel.answers))
        )
        questions_db = response.scalars().all()
        return [
            Question(
                id=question.id,
                title=question.title,
                theme_id=question.theme_id,
                answers=[
                    Answer(title=answer.title, is_correct=answer.is_correct)
                    for answer in question.answers
                ],
            )
            for question in questions_db
        ]
