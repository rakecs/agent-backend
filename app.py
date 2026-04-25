from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from fastapi.middleware.cors import CORSMiddleware
import os

# ---- Azure AI Foundry Setup ----
my_endpoint = "https://clinicexpert.services.ai.azure.com/api/projects/cliniexpert"
my_agent = "Agent457CliniExpert"
my_version = "2"

project_client = AIProjectClient(
    endpoint=my_endpoint,
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

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

# In-memory session store (simple)
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
def root():
    # Serve the index.html file
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "working"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        session_id = request.session_id
        message = request.message
        
        # Get or create thread for this session
        if session_id not in sessions:
            thread = openai_client.beta.threads.create()
            sessions[session_id] = thread.id
        
        thread_id = sessions[session_id]
        
        # Add user message to thread
        openai_client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        
        # Run the agent
        run = openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=my_agent
        )
        
        # Get the response
        if run.status == "completed":
            messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
            reply = messages.data[0].content[0].text.value
            return {"reply": reply}
        else:
            return {"error": f"Run status: {run.status}"}
            
    except Exception as e:
        return {"error": str(e)}
