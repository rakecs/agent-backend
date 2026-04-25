from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# ---- FastAPI App ----
app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    # Serve the index.html file
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "working", "message": "Static UI server running"}

@app.post("/chat")
def chat_disabled():
    return {"error": "Chat API is currently disabled. Only serving static UI."}
