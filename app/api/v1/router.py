from fastapi import APIRouter

from app.api.v1.endpoints import interview, janis, mindy

router = APIRouter()
router.include_router(interview.router, prefix="/interview", tags=["interview"])
router.include_router(janis.router, prefix="/janis", tags=["janis"])
router.include_router(mindy.router, prefix="/mindy", tags=["mindy"])
