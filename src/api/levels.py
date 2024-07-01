from fastapi import APIRouter

from src.repositories.levels import LevelsRepository
from src.schemas.levels import LevelSchema

router = APIRouter(
    prefix="/api/levels",
    tags=["Levels"],
)


@router.post('')
async def add_level(level: LevelSchema):
    levels_dict = level.model_dump()
    level_id = await LevelsRepository().add_one(levels_dict)
    return {"level_id": level_id}