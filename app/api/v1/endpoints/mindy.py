from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def mindy():
    return {"message": "Hello Mindy!"}
