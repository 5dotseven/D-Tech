from app.core.exceptions import ProviderUnavailableError
from app.core.llm.factory import create_provider
from app.repositories.interview import InMemorySessionRepository
from app.services.interview import InterviewService

_repo = InMemorySessionRepository()


def get_interview_service() -> InterviewService:
    try:
        return InterviewService(llm=create_provider(), repo=_repo)
    except RuntimeError as e:
        raise ProviderUnavailableError(str(e)) from e
