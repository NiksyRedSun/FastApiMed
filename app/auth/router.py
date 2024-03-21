import asyncio

from sqlalchemy import select, update
from fastapi import APIRouter, Request, Depends, FastAPI, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from .models import User
from ..database import get_async_session
from ..config import templates, base_url
from app.levels.models import *
from sqlalchemy.orm import selectinload
from app.gameplay.gameplay import GamePlay, gameplays

router = APIRouter(
    prefix="/dib_auth",
    tags=["dib_auth"]
)


# если все валидно, то эти функции вернут True, если нет, то вернут строку
async def validation_reg(email: str, user: str, password: str, password2: str, session):
    query = select(User).where(User.username == user)
    pre_result = await session.execute(query)
    result = pre_result.fetchall()
    if result:
        return "Пользователь с таким именем уже существует"
    if not email or not user or not password or not password2:
        return "Заполните все поля формы"
    if password != password2:
        return "Пароли не совпадают"
    if len(password) < 8:
        return 'Пароль должен содержать хотя бы 8 символов'
    return True



async def tables_for_user(id, session):
    async with session:
        inv = Inventory(user_id=id)
        wood_house = WoodHouse(user_id=id)
        hunter_house = HunterHouse(user_id=id)
        fields = Fields(user_id=id)
        town_square = TownSquare(user_id=id)
        war_house = WarHouse(user_id=id)
        market = Market(user_id=id)
        tower = Tower(user_id=id)
        bar = Bar(user_id=id)

        # можно создать список и передать его в add_all()
        session.add(inv)
        session.add(wood_house)
        session.add(hunter_house)
        session.add(fields)
        session.add(town_square)
        session.add(war_house)
        session.add(market)
        session.add(tower)
        session.add(bar)

        await session.commit()



@router.get("/login")
def login_get(request: Request, message: str = None, message_class: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "message": message, "message_class": message_class})


@router.post("/login")
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



@router.get("/register")
def register_get(request: Request, message: str = None, message_class: str = None):
    return templates.TemplateResponse("reg.html", {"request": request, "message": message, "message_class": message_class})



# Конечно костыль пздц, но ничего другого я пока не придумал
@router.post("/register")
async def register_post(request: Request, email: str = Form(default=''), password: str = Form(default=''), sec_password: str = Form(default=''),
                  username: str = Form(default=''), sqlsession: AsyncSession = Depends(get_async_session)):
    # try:
        res = await validation_reg(email, username, password, sec_password, sqlsession)
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
                response = await session.post(str(request.url_for('register:register')), json=data)

            if response.status != 400:
                res = await response.json()
                user_id = res['id']

                await tables_for_user(user_id, sqlsession)

                # loop = asyncio.get_event_loop()
                # gameplays[user_id] = GamePlay(user_id, sqlsession, loop)
                # gameplays[user_id].start_everything()


                return RedirectResponse(request.url_for('login_get').include_query_params(message='Регистрация успешна', message_class='success'), status_code=302)
            else:
                return RedirectResponse(
                    request.url_for('register_get').include_query_params(message='Пользователь с таким мылом уже существует', message_class='error'),
                    status_code=302)
        else:
            return RedirectResponse(request.url_for('register_get').include_query_params(message=res, message_class='error'), status_code=302)
    # except:
    #     return {
    #         "status": "error",
    #         "data": ":(",
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }

