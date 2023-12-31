from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["AdminPanel"], summary="Login admin")
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin = await self.store.admins.get_by_email(self.data["email"])
        if admin and admin.pass_valid_check(self.data["password"]):
            session = await new_session(request=self.request)
            admin_serialized = AdminSchema().dump(admin)
            session['admin'] = admin_serialized
            return json_response(data=admin_serialized)
        raise HTTPForbidden


class AdminCurrentView(View):
    @docs(tags=["AdminPanel"], summary="Get new user")
    @response_schema(AdminSchema, 200)
    async def get(self):
        if self.request.admin:
            return json_response(data=AdminSchema().dump(self.request.admin))
        else:
            raise HTTPUnauthorized
