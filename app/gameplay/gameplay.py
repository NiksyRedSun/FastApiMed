import asyncio
from app.auth.models import User
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session, async_session_maker
from app.levels.models import *
from sqlalchemy.orm import selectinload
from app.gameplay.spec_funcs import check_inv, model_by_slug, standart_level_up, level_to_up


gameplays = {}


async def start_game():
    session = async_session_maker()
    async with session:
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().fetchall()

        for user in users:
            loop = asyncio.get_event_loop()
            gameplays[user.id] = GamePlay(user.id, loop)
            gameplays[user.id].start_everything()



class GamePlay:

    def __init__(self, user_id, loop):
        self.user_id = user_id
        self.loop = loop


        self.town_square = None

        self.seconds_to_new_citizen = None
        self.seconds_to_new_knight = None
        self.seconds_to_new_archer = None

        self.seconds_to_money = None
        self.seconds_to_skins = None
        self.seconds_to_wood = None
        self.seconds_to_wheat = None

        self.seconds_to_upgrade = {
                            'town_square': None, 'wood_house': None, 'war_house': None, 'tower': None,
                             'market': None, 'hunter_house': None, 'fields': None, 'bar': None
        }

        self.money = 0


    async def get_obj_by_user_id(self, session: AsyncSession, obj_model):
        async with session:
            query = select(obj_model).where(obj_model.user_id == self.user_id)
            result = await session.execute(query)
            obj = result.scalar_one()
        return obj


    async def change_city_name(self, session: AsyncSession, city_name: str):
        town_square = await self.get_obj_by_user_id(session, TownSquare)
        town_square.city_name = city_name
        async with session:
            session.add(town_square)
            await session.commit()


    async def make_citizen(self):
        session = async_session_maker()
        while True:
            async with session:
                town_square = await self.get_obj_by_user_id(session, TownSquare)
                self.seconds_to_new_citizen = town_square.time_for_citizen


            while self.seconds_to_new_citizen > 0:
                if self.seconds_to_new_citizen >= 60:
                    print(f"До нового гражданина у игрока {self.user_id} осталось {int((self.seconds_to_new_citizen/60))} минуты")
                    await asyncio.sleep(60)
                    self.seconds_to_new_citizen -= 60
                else:
                    print(f"До нового гражданина у игрока {self.user_id} осталось меньше минуты")
                    await asyncio.sleep(self.seconds_to_new_citizen)
                    self.seconds_to_new_citizen = 0


            async with session:
                town_square = await self.get_obj_by_user_id(session, TownSquare)
                town_square.citizens_in_city += 1
                town_square.unemployed_citizens += 1
                print(f"Появился один житель у игрока {self.user_id}")
                print(f"Всего жителей у игрока {self.user_id}: {town_square.citizens_in_city}")
                await session.commit()



    async def make_money(self):
        session = async_session_maker()
        while True:
            async with session:
                town_square = await self.get_obj_by_user_id(session, TownSquare)
                self.seconds_to_money = town_square.time_for_money_pack
                money_pack = int(town_square.money_per_citizen * town_square.unemployed_citizens)


            while self.seconds_to_money > 0:
                if self.seconds_to_money >= 60:
                    print(f"До нового мешка с монетами у игрока {self.user_id} осталось {int((self.seconds_to_money / 60))} минуты")
                    await asyncio.sleep(60)
                    self.seconds_to_money -= 60
                else:
                    print(f"До нового мешка с монетами у игрока {self.user_id} осталось меньше минуты")
                    await asyncio.sleep(self.seconds_to_money)
                    self.seconds_to_money = 0


            async with session:
                inventory = await self.get_obj_by_user_id(session, Inventory)
                inventory.money += money_pack
                print(f"С горожан у игрока {self.user_id} собрано: {money_pack}")
                await session.commit()





    async def upgrade_level(self, level_slug):
        session = async_session_maker()
        async with session:
            level = await self.get_obj_by_user_id(session, model_by_slug[level_slug])

        self.seconds_to_upgrade[level_slug] = level.time_for_next_lvl


        while self.seconds_to_upgrade[level_slug] > 0:
            if self.seconds_to_upgrade[level_slug] >= 60:
                print(f"До улучшения {level_slug}  у игрока {self.user_id} осталось {int((self.seconds_to_upgrade[level_slug] / 60))} минуты")
                await asyncio.sleep(60)
                self.seconds_to_upgrade[level_slug] -= 60
            else:
                print(f"До обновления {level_slug}  у игрока {self.user_id} осталось меньше минуты")
                await asyncio.sleep(self.seconds_to_upgrade[level_slug])
                self.seconds_to_upgrade[level_slug] = 0

        self.seconds_to_upgrade[level_slug] = None


        async with session:
            level = await self.get_obj_by_user_id(session, model_by_slug[level_slug])
            level = level_to_up(level)
            session.add(level)
            print(f"Строение игрока {self.user_id} улучшено")
            await session.commit()



    def start_everything(self):
        self.loop.create_task(self.make_citizen())
        self.loop.create_task(self.make_money())










