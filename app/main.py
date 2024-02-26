import json

import uvicorn
from fastapi import APIRouter, Request, Depends, FastAPI, Form
from fastapi.responses import RedirectResponse
from .auth.base_config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate
from .menu.router import router as router_menu
from starlette.staticfiles import StaticFiles
from .config import templates
import requests




# если все валидно, то эта функция вернет True, если нет, то вернет строку
def validation(email: str, user: str, password: str, password2: str):
    if email[-3:] != '.ru' or '@' not in email:
        return "Мейл не соответствует правилам"
    if password != password2:
        return "Пароли не совпадают"
    if len(password) < 8:
        return 'Пароль должен содержать хотя бы 8 символов'
    return True



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


@app.get("/login")
def login_get(request: Request, message: str = None, message_class: str = None):

    return templates.TemplateResponse("login.html", {"request": request, "message": message, "message_class": message_class})

@app.post("/login")
def login_post(request: Request, message=None):
    return templates.TemplateResponse("login.html", {"request": request, "message": message})


@app.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})


# Конечно костыль пздц, но ничего другого я пока не придумал
@app.post("/register")
def register_post(request: Request, email: str = Form(...), password: str = Form(...), sec_password: str = Form(...), username: str = Form(...)):
    try:
        res = validation(email, username, password, sec_password)
        if type(res) != str:
            data={
                  "email": email,
                  "password": password,
                  "is_active": True,
                  "is_superuser": False,
                  "is_verified": False,
                  "username": username
                }

            r = requests.request("POST", data=json.dumps(data), url=str(request.base_url)[:-1] + app.url_path_for('register:register'))
            return RedirectResponse(request.url_for('login_get').include_query_params(message='Регистрация успешна', message_class='success'))
    except:
        pass

app.include_router(router_menu)
# uvicorn app.main:app --reload
