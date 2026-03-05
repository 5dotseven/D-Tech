from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.constants import LEVELS, ROLES
from app.dependencies import get_interview_service
from app.schemas.interview import (
    AnswerRequest,
    AnswerResponse,
    OptionsResponse,
    ResultResponse,
    SetupRequest,
    SetupResponse,
)
from app.services.interview import InterviewService

router = APIRouter()


@router.get("/options", response_model=OptionsResponse)
async def get_options():
    return OptionsResponse(roles=ROLES, levels=[lv.value for lv in LEVELS])


@router.post("/setup", response_model=SetupResponse)
async def setup_interview(
    req: SetupRequest,
    service: Annotated[InterviewService, Depends(get_interview_service)],
):
    session = await service.start(req.role, req.framework, req.extras, req.level)
    return SetupResponse(
        session_id=session.session_id,
        question_number=session.question_count,
        question=session.last_message,
    )


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    req: AnswerRequest,
    service: Annotated[InterviewService, Depends(get_interview_service)],
):
    session = await service.answer(req.session_id, req.answer)
    if session.is_finished:
        return AnswerResponse(
            session_id=session.session_id,
            finished=True,
            result=session.result,
        )
    return AnswerResponse(
        session_id=session.session_id,
        finished=False,
        question_number=session.question_count,
        question=session.last_message,
    )


@router.get("/result/{session_id}", response_model=ResultResponse)
async def get_result(
    session_id: str,
    service: Annotated[InterviewService, Depends(get_interview_service)],
):
    session = service.get_result(session_id)
    return ResultResponse(
        session_id=session_id,
        setup={
            "role": session.role,
            "framework": session.framework,
            "extras": session.extras,
            "level": session.level,
        },
        result=session.result,
    )
