# from fastapi import APIRouter
# from globals import global_settings
# from src.services.admin import AdminPanel
#
# router = APIRouter(
#     prefix="/api/user",
#     tags=["Settings"],
# )
#
#
# @router.post('')
# async def change_settings_router():
#     await AdminPanel().get_settings()
#     heats = AdminPanel().get_setting_value("heats")
#     print(f"value for heats: {heats}")
#     return global_settings
