from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def janis():
    return {"message": "Hello Janis!"}
