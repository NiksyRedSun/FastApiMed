import json

import uvicorn
from fastapi import APIRouter, Request, Depends, FastAPI, Form

from .auth.base_config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate
from .menu.router import router as router_menu
from starlette.staticfiles import StaticFiles
from .config import templates
import requests



app = FastAPI(
    title="Trading App"
)

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
def get_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})



@app.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})



@app.post("/register")
def register_post(request: Request, email: str = Form(...), password: str = Form(...)):
    data={
          "email": email,
          "password": password,
          "is_active": True,
          "is_superuser": False,
          "is_verified": False,
          "username": "AnotherAnyUserName"
        }

    r = requests.request("POST", data=json.dumps(data), url=str(request.base_url)[:-1] + app.url_path_for('register:register'))
    print(r)

app.include_router(router_menu)
# uvicorn app.main:app --reload
