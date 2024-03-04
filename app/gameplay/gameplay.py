import asyncio
from app.auth.models import User
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.levels.models import *
from sqlalchemy.orm import selectinload


gameplays = {}

class GamePlay:

    def __init__(self, user_id):
        self.user_id = user_id

        # self.event_loop = asyncio.new_event_loop()
        # self.event_loop.run_forever()

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

        self.new_peasant_task = None
        self.new_knight_task = None
        self.new_archer_task = None

        self.minutes_to_new_peasant = None
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

        self.money = 0


    async def make_money(self):
        while True:
            seconds = 150
            while seconds > 0:
                if seconds >= 60:
                    print(f"До монеты осталось {int((seconds/60))} минуты")
                    await asyncio.sleep(60)
                    seconds -= 60
                else:
                    print(f"До монеты осталось меньше минуты")
                    await asyncio.sleep(seconds)
                    seconds = 0
            self.money += 1
            print("Заработана одна монетка")
            print(f"Всего монет: {self.money}")






