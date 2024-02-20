import uvicorn
from fastapi import APIRouter, Request, Depends, FastAPI
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from .auth.base_config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate


app = FastAPI(
    title="Trading App"
)


templates = Jinja2Templates(directory="app/templates")
app.mount("/app/static", StaticFiles(directory="app/static", html=True), name="static")



# Ниже два роутера - для аутентификации и регистрации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/")
def get_base_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})



# uvicorn app.main:app --reload
