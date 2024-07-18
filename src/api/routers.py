from ..api.levels import router as levels_router
from ..api.users import router as users_router
from ..api.rating import router as rating_router
from ..api.setings import router as settings_router
from ..api.auth import router as auth_router
from ..api.gift import router as gift_router

all_routers = [
    levels_router,
    users_router,
    rating_router,
    settings_router,
    auth_router,
    gift_router
]
