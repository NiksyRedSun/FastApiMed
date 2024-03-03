from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import templates

from ..database import get_async_session
from .models import Menu
# from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


level_info = {'bar': {'name': 'Таверна', 'img_link': 'images\cards\\256\\bar.png', 'descr': 'В этой таверне собираются местные егеря, когда устают от шума леса и одиночества. Соответственно здесь можно найти очень много ловких людей, умеющих обращаться с луком и стрелами'},
              'fields': {'name': 'Поля', 'img_link': 'images\cards\\256\\fields.png', 'descr': 'Ваш хлеб насущный.'},
              'hunter_house': {'name': 'Лачуга охотника', 'img_link': 'images\cards\\256\\hunter_house.png', 'descr': 'Лачуга старого охотника. Что он делал до пенсии - лучше не знать. Сейчас же он обучает население соответствующему ремеслу'},
              'market': {'name': 'Рынок', 'img_link': 'images\cards\\256\\market.png', 'descr': 'Рыночный квартал. Позволяет обменивать различные ресурсы.'},
              'tower': {'name': 'Сторожевая башня', 'img_link': 'images\cards\\256\\tower.png', 'descr': 'Сторожевая башня. Чтобы наблюдать, не наблюдает ли кто-нибудь за вами.'},
              'town_square': {'name': 'Городская площадь', 'img_link': 'images\cards\\256\\town_square.png', 'descr': 'Городская площадь, здесь собираются крестьяне из окрестных деревень.'},
              'war_house': {'name': 'Казармы', 'img_link': 'images\cards\\256\\war_house.png', 'descr': 'В этих казармах взрослые мужчины, озабоченные рыцарским делом, способствуют росту своего мастерства.'},
              'wood_house': {'name': 'Дом дровосека', 'img_link': 'images\cards\\256\\wood_house.png', 'descr': 'Хозяин не любит появляться на людях. Люди не любят, встречаться с хозяином. Поэтому он живет здесь, всем от этого хорошо.'}
              }



#
@router.get("/{slug}")
async def get_menu_item(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # pre_result = await session.execute(select(Menu).where(Menu.slug==slug))
        # запомни, sqlalch всегда возвращает кортеж, поэтому в дальнейшем нужно обращаться именно к одному элементу
        # result = pre_result.fetchone()
        return templates.TemplateResponse("menu_item.html", {"request": request, "menu_par": level_info[slug]})

    except Exception as e:
        return {
            "status": "error",
            "data": e,
            "details": None
        }


