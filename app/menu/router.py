from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import templates
from app.auth.models import User
from app.auth.base_config import auth_backend, fastapi_users, current_user
from fastapi.responses import RedirectResponse
from ..database import get_async_session
# from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


level_info = {'bar': {'name': 'Таверна', 'img_link': 'images/cards/256/bar.png', 'slug': 'bar',
                        'cit_img': 'images/persons/archer.png', 'cit_name': 'Лучник',
                      'descr': 'В этой таверне собираются местные егеря, когда устают от шума леса и одиночества. Соответственно здесь можно найти очень много ловких людей, умеющих обращаться с луком и стрелами. Улучшение казарм ускоряет тренировку лучников и увеличивает их максимальное количество.'},

              'fields': {'name': 'Поля', 'img_link': 'images/cards/256/fields.png', 'slug': 'fields',
                         'cit_img': 'images/persons/peasant.png', 'cit_name': 'Крестьянин',
                         'descr': 'Крестьяне думали, что, придя в город, избавятся от необходимости копаться в земле. Улучшите поля и у вас получится собирать больше пшена за меньшее время.'},

              'hunter_house': {'name': 'Лачуга охотника', 'img_link': 'images/cards/256/hunter_house.png', 'slug': 'hunter_house',
                            'cit_img': 'images/persons/huntsman.png', 'cit_name': 'Охотник',
                               'descr': 'Лачуга старого охотника. Что он делал до пенсии - лучше не знать. Сейчас же он обучает население соответствующему ремеслу. Улучшите их и у вас получится собирать больше шкур за меньшее время.'},

              'wood_house': {'name': 'Дом лесоруба', 'img_link': 'images/cards/256/wood_house.png', 'slug': 'wood_house',
                                'cit_img': 'images/persons/woodman.png', 'cit_name': 'Дровосек',
                             'descr': 'Хозяин не любит появляться на людях. Люди не любят, встречаться с хозяином. Поэтому он живет здесь, всем от этого хорошо. Улучшите лачугу и у вас получится собирать больше дерева за меньшее время.'},

              'market': {'name': 'Рынок', 'img_link': 'images/cards/256/market.png', 'slug': 'market',
                         'descr': 'Рыночный квартал. Позволяет обменивать различные ресурсы. Улучшение рынка снизит налоги на обмен товаров.'},

              'tower': {'name': 'Сторожевая башня', 'img_link': 'images/cards/256/tower.png', 'slug': 'tower',
                        'descr': 'Сторожевая башня. Чтобы наблюдать, не наблюдает ли кто-нибудь за вами. Улучшение сторожевой башни приведет к уменьшению времени, которое потребуется чтобы добраться до других игроков.'},

              'town_square': {'name': 'Городская площадь', 'img_link': 'images/cards/256/town_square.png', 'slug': 'town_square',
                              'descr': 'Городская площадь, здесь собираются крестьяне из окрестных деревень, превращаясь в горожан. Улучшите городскую площадь и вы будете привлекать больше крестьян, а также собирать с них больше налогов за меньшее время.'},

              'war_house': {'name': 'Казармы', 'img_link': 'images/cards/256/war_house.png', 'slug': 'war_house',
                            'cit_img': 'images/persons/knight.png', 'cit_name': 'Рыцарь',
                            'descr': 'В этих казармах взрослые мужчины, озабоченные рыцарским делом, способствуют росту своего мастерства. Улучшение казарм приведет к увеличению максимальной численности рыцарей и ускорению их тренировок.'}
              }




def get_user_info(slug: str, ):
    pass

@router.get("/{slug}")
async def get_menu_item(request: Request, slug: str, session: AsyncSession = Depends(get_async_session),  user: User | None = Depends(current_user)):
    # try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            return templates.TemplateResponse(f"menu_items/{slug}.html", {"request": request, "menu_par": level_info[slug]})


    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "data": e,
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }


