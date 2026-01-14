from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.api.routes_predict import router as predict_router
from app.api.routes_alerts import router as alerts_router
from app.api.routes_cases import router as cases_router


app = FastAPI(title="Bank Chatbot API")

@app.get("/")
def home():
    return {"message": "Bank Chatbot API is running. Go to /docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(alerts_router)
app.include_router(cases_router)