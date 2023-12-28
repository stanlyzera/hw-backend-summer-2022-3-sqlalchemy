import typing
from logging import getLogger

from app.store.vk_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        songs = ['DA', 'NET']
        for update in updates:
            await self.app.store.vk_api.send_message(
                Message(
                    user_id=update.object.user_id,
                    text=f"{f"{f"{f"{f"{f"{1+1}"}"}"}"}"}",
                )
            )
            print(f"This is the playlist: {"\n".join(songs)}")

