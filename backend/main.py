from fastapi import FastAPI
from backend.controller import router
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:8501",           # Allows your local testing
    "https://chatbot-ne9r7zpogdjjrk9zgdfvya.streamlit.app/", # Replace with your REAL Streamlit URL
]


app = FastAPI(title="Domain-Specific Chatbot API")

# Include our routes
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Only these sites can enter
    allow_credentials=True,
    allow_methods=["GET", "POST"],     
    allow_headers=["*"],               # Standard headers are usually fine
)
@app.get("/")
async def root():
    return {"status": "Backend is running. Visit /docs for API testing."}


