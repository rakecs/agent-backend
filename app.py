from fastapi import FastAPI
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from fastapi.middleware.cors import CORSMiddleware

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
    return {"status": "ok"}

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id

    if session_id not in sessions:
        sessions[session_id] = []

    conversation = sessions[session_id]
    conversation.append({"role": "user", "content": req.message})

    try:
        response = openai_client.responses.create(
            input=conversation,
            extra_body={
                "agent_reference": {
                    "name": my_agent,
                    "version": my_version,
                    "type": "agent_reference",
                }
            },
        )

        reply = response.output_text

        conversation.append({"role": "assistant", "content": reply})

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}