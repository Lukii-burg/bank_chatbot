from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes_auth import router as auth_router
from app.api.routes_predict import router as predict_router
from app.api.routes_alerts import router as alerts_router
from app.api.routes_cases import router as cases_router
from app.api.routes_chat import router as chat_router


app = FastAPI(title="Bank Chatbot API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
app.include_router(chat_router)