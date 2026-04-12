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
    return {"status": "working"}



    except Exception as e:
        return {"error": str(e)}