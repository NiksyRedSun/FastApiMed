import asyncio
from app.auth.models import User
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session, async_session_maker
from app.levels.models import *
from sqlalchemy.orm import selectinload



gameplays = {}


async def start_game():
    session = async_session_maker()
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().fetchall()
    await session.close()
    for user in users:
        loop = asyncio.get_event_loop()
        gameplays[user.id] = GamePlay(user.id, loop)
        gameplays[user.id].start_everything()





class GamePlay:

    def __init__(self, user_id, loop):
        self.user_id = user_id
        self.loop = loop


        self.bar_upgrade_task = None
        self.fields_upgrade_task = None
        self.hunter_house_upgrade_task = None
        self.market_upgrade_task = None
        self.tower_upgrade_task = None
        self.town_square_upgrade_task = None
        self.war_house_upgrade_task = None
        self.wood_house_upgrade_task = None

        self.minutes_to_bar_upgrade = None
        self.minutes_to_fields_upgrade = None
        self.minutes_to_hunter_house_upgrade = None
        self.minutes_to_market_upgrade = None
        self.minutes_to_tower_upgrade = None
        self.minutes_to_town_square_upgrade = None
        self.minutes_to_war_house_upgrade = None
        self.minutes_to_wood_house_upgrade = None

        self.new_citizen_task = None
        self.new_knight_task = None
        self.new_archer_task = None

        self.minutes_to_new_citizen = None
        self.minutes_to_new_knight = None
        self.minutes_to_new_archer = None

        self.skins_task = None
        self.money_task = None
        self.wood_task = None
        self.wheat_task = None

        self.minutes_to_skins = None
        self.minutes_to_money = None
        self.minutes_to_wood = None
        self.minutes_to_wheat = None

        self.town_square = None

        self.money = 0


    async def make_citizen(self):
        session = async_session_maker()
        while True:
            async with session:
                query = select(TownSquare).where(TownSquare.user_id == self.user_id)
                result = await session.execute(query)
                town_square = result.scalar_one()
                seconds = town_square.time_for_citizen


            while seconds > 0:
                if seconds >= 60:
                    print(f"До нового гражданина у игрока {self.user_id} осталось {int((seconds/60))} минуты")
                    await asyncio.sleep(60)
                    seconds -= 60
                else:
                    print(f"До нового гражданина у игрока {self.user_id} осталось меньше минуты")
                    await asyncio.sleep(seconds)
                    seconds = 0

            async with session:
                query = select(TownSquare).where(TownSquare.user_id == self.user_id)
                result = await session.execute(query)
                town_square = result.scalar_one()
                town_square.citizens_in_city += 1
                town_square.unemployed_citizens += 1
                print(f"Появился один житель у игрока {self.user_id}")
                print(f"Всего жителей у игрока {self.user_id}: {town_square.citizens_in_city}")
                await session.commit()


    async def make_money(self):
        session = async_session_maker()
        while True:
            async with session:
                query = select(TownSquare).where(TownSquare.user_id == self.user_id)
                result = await session.execute(query)
                town_square = result.scalar_one()
                seconds = town_square.time_for_money_pack
                money_pack = int(town_square.money_per_citizen * town_square.unemployed_citizens)

            while seconds > 0:
                if seconds >= 60:
                    print(f"До нового мешка с монетами у игрока {self.user_id} осталось {int((seconds / 60))} минуты")
                    await asyncio.sleep(60)
                    seconds -= 60
                else:
                    print(f"До нового мешка с монетами у игрока {self.user_id} осталось меньше минуты")
                    await asyncio.sleep(seconds)
                    seconds = 0

            async with session:
                query = select(Inventory).where(Inventory.user_id == self.user_id)
                result = await session.execute(query)
                inventory = result.scalar_one()
                inventory.money += money_pack
                print(f"С горожан у игрока {self.user_id} собрано: {money_pack}")
                await session.commit()


    def start_everything(self):
        self.loop.create_task(self.make_citizen())
        self.loop.create_task(self.make_money())










