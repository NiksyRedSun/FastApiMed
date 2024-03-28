from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import templates
from app.auth.models import User
from app.levels.models import *
from app.gameplay.gameplay import gameplays
from app.gameplay.spec_funcs import seconds_to_minutes, seconds_to_minutes_in_nums
from app.gameplay.spec_funcs import model_by_slug







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






async def make_context(session: AsyncSession, user: User, slug: str = None):
    dict_context = dict()
    gameplay = gameplays[user.id]

    #функции
    dict_context["secs_to_mins"] = seconds_to_minutes
    dict_context["secs_to_mins_in_nums"] = seconds_to_minutes_in_nums

    #инвентарь
    async with session:
        inventory = await gameplay.get_obj_by_user_id(session, Inventory)
        dict_context['inventory'] = inventory

    #материал по уровням
    if slug is not None:
        dict_context['level_info'] = level_info[slug]
        dict_context['level_slug'] = slug

        async with session:
            dict_context['level'] = await gameplay.get_obj_by_user_id(session, model_by_slug[slug])

        #в зависимости от уровня
        if slug == 'town_square':
            dict_context['secs_to_cit'] = gameplay.seconds_to_new_citizen
            dict_context['secs_to_money'] = gameplay.seconds_to_money

        elif slug == 'war_house':
            pass



    return dict_context
