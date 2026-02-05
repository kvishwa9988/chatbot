from fastapi import FastAPI
from backend.controller import router

app = FastAPI(title="Domain-Specific Chatbot API")

# Include our routes
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "Backend is running. Visit /docs for API testing."}