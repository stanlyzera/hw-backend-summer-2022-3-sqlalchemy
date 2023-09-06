import typing
from hashlib import sha256
from typing import Optional

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor


if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        self.app = app
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        query = select(AdminModel).where(AdminModel.email == email)
        response = await self.app.database.orm_select(query=query)
        admin = response.scalar()
        if admin:
            return Admin(id=admin.id, email=admin.email, password=admin.password)

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = AdminModel(email=email, password=sha256(password.encode()).hexdigest())
        await self.app.database.orm_add(admin)
