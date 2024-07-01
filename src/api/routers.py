from ..api.levels import router as levels_router
from ..api.users import router as users_router
from ..api.rating import router as rating_router


all_routers = [
    levels_router,
    users_router,
    rating_router
]