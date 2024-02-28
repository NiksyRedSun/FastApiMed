import json
from sqlalchemy import select, insert
import uvicorn
from fastapi import APIRouter, Request, Depends, FastAPI, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from .auth.models import User
from .database import get_async_session
from .auth.base_config import auth_backend, fastapi_users, current_user
from .auth.schemas import UserRead, UserCreate
from .menu.router import router as router_menu
from starlette.staticfiles import StaticFiles
from .config import templates
from .auth.utils import get_user_db

import requests
from pydantic import ValidationError




# если все валидно, то эти функции вернут True, если нет, то вернут строку
async def validation_reg(email: str, user: str, password: str, password2: str, session):
    query = select(User).where(User.username == user)
    pre_result = await session.execute(query)
    result = pre_result.fetchall()
    if result:
        return "Пользователь с таким именем уже существует"
    if not email or not user or not password or not password2:
        return "Заполните все поля формы"
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
def get_menu(request: Request, user: User | None = Depends(current_user)):
    try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            return templates.TemplateResponse("menu.html", {"request": request})
    except:
        return {
            "status": "error",
            "data": ":(",
            "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
        }


@app.get("/login")
def login_get(request: Request, message: str = None, message_class: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "message": message, "message_class": message_class})


@app.post("/login")
async def login_post(request: Request, email: str = Form(default=''), password: str = Form(default='')):
    try:

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=f'{request.base_url}auth/jwt/login',
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                data={
                    'username': email,
                    'password': password
                },
            )
        if response.status == 400:
            return RedirectResponse(request.url_for('login_get').include_query_params(
                    message='Неправильный логин или пароль', message_class='error'),
                status_code=302)

        redirect = RedirectResponse(url=f'{request.base_url}', status_code=302)
        redirect.set_cookie(key='authepta', value=response.cookies.get('authepta'), httponly=True)

        return redirect

    except:
        return {
            "status": "error",
            "data": ":(",
            "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
        }



@app.get("/register")
def register_get(request: Request, message: str = None, message_class: str = None):
    return templates.TemplateResponse("reg.html", {"request": request, "message": message, "message_class": message_class})


# Конечно костыль пздц, но ничего другого я пока не придумал
@app.post("/register")
async def register_post(request: Request, email: str = Form(default=''), password: str = Form(default=''), sec_password: str = Form(default=''),
                  username: str = Form(default=''), session: AsyncSession = Depends(get_async_session)):
    try:
        res = await validation_reg(email, username, password, sec_password, session)
        if type(res) != str:
            data = {
                  "email": email,
                  "password": password,
                  "is_active": True,
                  "is_superuser": False,
                  "is_verified": False,
                  "username": username
                }

            async with aiohttp.ClientSession() as session:
                response = await session.post(str(request.base_url)[:-1] + app.url_path_for('register:register'), json=data)

            # r = requests.request("POST", data=json.dumps(data), url=str(request.base_url)[:-1] + app.url_path_for('register:register'), allow_redirects=True)
            if response.status != 400:
                return RedirectResponse(request.url_for('login_get').include_query_params(message='Регистрация успешна', message_class='success'), status_code=302)
            else:
                return RedirectResponse(
                    request.url_for('register_get').include_query_params(message='Пользователь с таким мылом уже существует', message_class='error'),
                    status_code=302)
        else:
            return RedirectResponse(request.url_for('register_get').include_query_params(message=res, message_class='error'), status_code=302)
    except:
        return {
            "status": "error",
            "data": ":(",
            "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
        }



app.include_router(router_menu)


# uvicorn app.main:app --reload
