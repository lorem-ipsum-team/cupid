from fastapi import APIRouter
from . import recommendation

router = APIRouter()
router.include_router(recommendation.router, prefix='/recommend')
