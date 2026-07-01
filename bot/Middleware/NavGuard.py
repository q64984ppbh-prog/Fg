from aiogram.types import Message, TelegramObject
from aiogram.fsm.context import FSMContext
from typing import Any, Awaitable, Callable, Dict

NAV_BUTTONS = {'💸 Баланс', '🎮 Играть', '🏠 Меню'}

class NavGuard:
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.text and event.text in NAV_BUTTONS:
            state: FSMContext = data.get("state")
            if state:
                await state.clear()
        return await handler(event, data)
