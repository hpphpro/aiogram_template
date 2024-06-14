from typing import Any, Dict, Final, Optional

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import I18n, I18nMiddleware
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from src.common.di import Depends, inject
from src.core.settings import path
from src.database.gateway import DBGateway
from src.database.models import User

DEFAULT_LOCALE_PATH: str = path("locales")
DEFAULT_LOCALE: Final[str] = "en"

try:
    import babel  # noqa

    i18n = I18n(path=DEFAULT_LOCALE_PATH, default_locale=DEFAULT_LOCALE)
    simple_locale_middleware = SimpleI18nMiddleware(i18n)

    gettext = i18n.gettext
except ImportError:
    pass


def _user_id_from_data(data: Dict[str, Any]) -> Optional[int]:
    return user.id if (user := data.get("event_from_user")) else None


@inject
async def _get_db_user(user_id: int, gateway: DBGateway = Depends()) -> Optional[User]:
    return await gateway.user().select(user_id)


class Localization(I18nMiddleware):
    async def get_locale(
        self, event: types.TelegramObject, data: Dict[str, Any]
    ) -> str:
        state: FSMContext = data["state"]
        language = (await state.get_data()).get("_language_code")
        if not language:
            user_id = _user_id_from_data(data)
            if not user_id:
                language = data["locale"] = self.i18n.default_locale
            else:
                user = await _get_db_user(user_id)
                if not user:
                    language = data["locale"] = self.i18n.default_locale
                else:
                    language = data["locale"] = (
                        user.language_code or self.i18n.default_locale
                    )
            await state.update_data(_language_code=language)

        return language
