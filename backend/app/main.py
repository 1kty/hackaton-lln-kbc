from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError

from backend.app.chat import generate_reply
from backend.app.customers import get_customer, get_transactions
from backend.app.schemas import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(title="KBC Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_customer(client_id: str) -> dict:
    try:
        customer = get_customer(client_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/customers/{client_id}")
def customer_profile(client_id: str) -> dict:
    customer = load_customer(client_id)
    customer["transactions"] = get_transactions(client_id)
    return customer


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    customer = load_customer(request.client_id)
    customer["transactions"] = get_transactions(request.client_id)
    try:
        reply = generate_reply(request.message, customer, request.history)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OpenAIError as exc:
        raise HTTPException(status_code=503, detail="AI provider error") from exc
    return ChatResponse(reply=reply, client_id=request.client_id)
