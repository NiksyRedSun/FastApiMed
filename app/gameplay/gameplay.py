import asyncio
from app.auth.models import User
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session, async_session_maker
from app.levels.models import *
from sqlalchemy.orm import selectinload
from app.gameplay.spec_funcs import check_inv, model_by_slug, standart_level_up, level_to_up


gameplays = {}

name_by_slug = {'town_square': 'Городская площадь', 'war_house':'Казармы', 'bar': 'Таверна', 'market': 'Рынок',
                'fields': 'Поля', 'hunter_house': 'Лачуга охотника', 'wood_house': 'Дом лесоруба', 'tower': 'Сторожевая башня'}

def message_check(message: Message):
    message.is_checked = True
    return message


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
        async with session:
            town_square = await self.get_obj_by_user_id(session, TownSquare)
            town_square.city_name = city_name
            session.add(town_square)
            await session.commit()


    # вернет true - если все круто, вернет str, если есть проблемы
    async def distribute_workers(self, session: AsyncSession, citizens: int, workers: int, model):
        town_square = await self.get_obj_by_user_id(session, TownSquare)
        work_house = await self.get_obj_by_user_id(session, model)

        if workers == 0 and citizens == 0:
            return "Лучше не оставлять нули везде"

        if workers + citizens != town_square.unemployed_citizens + work_house.workers:
            return "Что-то не так с расчетами, попробуйте еще раз"

        async with session:
            work_house.workers = workers
            town_square.unemployed_citizens = citizens
            session.add(work_house)
            session.add(town_square)
            await session.commit()
        return True


    # вернет true - если все круто, вернет str, если есть проблемы
    async def get_workers_from_model(self, session: AsyncSession, model, workers: int):
        work_house = await self.get_obj_by_user_id(session, model)
        if workers > work_house.workers:
            return "У вас нет стольких работников"
        town_square = await self.get_obj_by_user_id(session, TownSquare)
        async with session:
            work_house.workers -= workers
            town_square.unemployed_citizens += workers
            session.add(work_house)
            session.add(town_square)
            await session.commit()
        return True


    async def make_citizen(self):
        session = async_session_maker()
        while True:
            async with session:
                town_square = await self.get_obj_by_user_id(session, TownSquare)


            if town_square.citizens_in_city >= town_square.max_citizens:
                await asyncio.sleep(60)
                print(f"У игрока {self.user_id} - максимум граждан")
                self.seconds_to_new_citizen = None

            else:
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
                    session.add(town_square)
                    print(f"Появился один гражданин у игрока {self.user_id}")
                    print(f"Всего граждан у игрока {self.user_id}: {town_square.citizens_in_city}")
                    await session.commit()



    async def make_message(self, session: AsyncSession, message_class: str, message: str):
        async with session:
            message = Message(user_id=self.user_id, text=message, message_class=message_class)
            session.add(message)
            await session.commit()


    #Как только отрабатывает эта функция - пользователь обязан попадать на страницу сообщений,
    # поскольку все сообщения переходят в прочитанные
    async def get_messages(self, session: AsyncSession):
        async with session:
            query = select(Message).where(Message.user_id == self.user_id)
            result = await session.execute(query)
            messages = result.scalars().all()
            messages = list(map(message_check, messages))
            session.add_all(messages)
            await session.commit()
        return messages



    async def get_count_unread_messages(self, session: AsyncSession):
        async with session:
            query = select(Message).where((Message.user_id == self.user_id) & (Message.is_checked == False))
            count_query = select(func.count()).select_from(query.subquery())
            result = await session.execute(count_query)
        return result.scalar()



    async def make_money(self):
        session = async_session_maker()
        while True:
            async with session:
                town_square = await self.get_obj_by_user_id(session, TownSquare)
                money_pack = town_square.money_per_citizen * town_square.unemployed_citizens


            print(f"До нового мешка с монетами у игрока {self.user_id} осталось 60 секунд")
            await asyncio.sleep(60)


            async with session:
                inventory = await self.get_obj_by_user_id(session, Inventory)
                inventory.money += round(money_pack/60, 2)
                session.add(inventory)
                print(f"С горожан у игрока {self.user_id} собрано: {round(money_pack/60, 2)}")
                await session.commit()


    async def make_wood(self):
        session = async_session_maker()
        while True:
            async with session:
                wood_house = await self.get_obj_by_user_id(session, WoodHouse)
                wood_pack = wood_house.res_per_worker * wood_house.workers


            print(f"До нового мешка с дровами у игрока {self.user_id} осталось 60 секунд")
            await asyncio.sleep(60)


            async with session:
                inventory = await self.get_obj_by_user_id(session, Inventory)
                inventory.wood += round(wood_pack/60, 2)
                session.add(inventory)
                print(f"Горожане собрали {round(wood_pack/60, 2)} дерева")
                await session.commit()





    async def make_wheat(self):
        session = async_session_maker()
        while True:
            async with session:
                fields = await self.get_obj_by_user_id(session, Fields)
                wheat_pack = fields.res_per_worker * fields.workers


            print(f"До нового мешка с пшеном у игрока {self.user_id} осталось 60 секунд")
            await asyncio.sleep(60)


            async with session:
                inventory = await self.get_obj_by_user_id(session, Inventory)
                inventory.wheat += round(wheat_pack/60, 2)
                session.add(inventory)
                print(f"Горожане собрали {round(wheat_pack/60, 2)} пшена")
                await session.commit()



    async def make_skins(self):
        session = async_session_maker()
        while True:
            async with session:
                hunter_house = await self.get_obj_by_user_id(session, HunterHouse)
                skins_pack = hunter_house.res_per_worker * hunter_house.workers


            print(f"До нового мешка с шкурами у игрока {self.user_id} осталось 60 секунд")
            await asyncio.sleep(60)


            async with session:
                inventory = await self.get_obj_by_user_id(session, Inventory)
                inventory.skins += round(skins_pack/60, 2)
                session.add(inventory)
                print(f"Горожане собрали {round(skins_pack/60, 2)} шкур")
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

        await self.make_message(session, "build", f"Здание {name_by_slug[level_slug]} улучшено до уровня {level.cur_level}")



    def start_everything(self):
        self.loop.create_task(self.make_citizen())
        self.loop.create_task(self.make_money())
        self.loop.create_task(self.make_wood())
        self.loop.create_task(self.make_wheat())
        self.loop.create_task(self.make_skins())










