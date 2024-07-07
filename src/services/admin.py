from src.repositories.settings import AdminRepository
from globals import global_settings


class AdminPanel():

    @staticmethod
    async def get_settings():
        settings = await AdminRepository().get_all()
        await AdminPanel().load_global_settings(settings)

    @staticmethod
    async def load_global_settings(settings):
        global global_settings
        global_settings.clear()
        for setting in settings:
            global_settings[setting.key] = setting.value

    @staticmethod
    def get_setting_value(key: str) -> int:
        return global_settings.get(key)
