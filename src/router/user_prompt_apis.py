import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Body
from fastapi.responses import StreamingResponse


from container import Container
from model.user_prompt_model import UserPromptQueryRequest
from service.prompt_service import PromptService
from utils.utility_contants import UtilityConstant


router = APIRouter(
    tags=["user_prompts"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/chat_completions",
    response_class=StreamingResponse,
    summary="Respond to user prompt with context",
)
@inject
def get_prompt_response(
    request: UserPromptQueryRequest = Body(...),
    prompt_service: PromptService = Depends(Provide[Container.prompt_service]),
):
    try:
        response = prompt_service.get_prompt_response(
            request.user_prompt, request.conversation_id
        )
        return StreamingResponse(response, media_type="text/event-stream")
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UtilityConstant.INTERNAL_SERVER_ERROR + str(e),
        )
