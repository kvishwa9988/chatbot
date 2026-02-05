from fastapi import APIRouter
from .models import ChatRequest, ChatResponse
from .service import ChatService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Pass request data to the Service layer
    bot_output = ChatService.run_chat(request.session_id, request.message)
    return ChatResponse(output=bot_output)