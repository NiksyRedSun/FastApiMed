from app.levels.models import *
from sqlalchemy.ext.asyncio import AsyncSession

model_by_slug = {'town_square': TownSquare, 'wood_house': WoodHouse, 'war_house': WarHouse, 'tower': Tower,
                 'market': Market, 'hunter_house': HunterHouse, 'fields': Fields, 'bar': Bar}




def seconds_to_minutes(seconds):
    if seconds > 60:
        minutes = seconds // 60
        half_minutes = minutes % 10
        if minutes == 10:
            return "10 минут"
        elif minutes == 11:
            return "11 минут"
        elif minutes == 12:
            return "12 минут"
        elif minutes == 13:
            return f"13 минут"
        elif minutes == 14:
            return f"14 минут"
        elif minutes == 1:
            return "1 минута"
        elif minutes == 21:
            return "21 минута"
        elif 2 <= half_minutes <= 4:
            return f"{minutes} минуты"
        else:
            return f"{minutes} минут"
    else:
        return 'меньше минуты'


def seconds_to_minutes_in_nums(seconds):
    minutes = seconds // 60
    if minutes < 10:
        if minutes == 0:
            minutes = '00'
        else:
            minutes = f"0{minutes}"
    seconds = seconds % 60
    if seconds < 10:
        if seconds == 0:
            seconds = '00'
        else:
            seconds = f"0{seconds}"
    return f'{minutes}:{seconds}'



def check_inv(level, inventory: Inventory):
    if hasattr(level, 'money_for_next_lvl'):
        if inventory.money < level.money_for_next_lvl:
            return False
    if hasattr(level, 'wheat_for_next_lvl'):
        if inventory.wheat < level.wheat_for_next_lvl:
            return False
    if hasattr(level, 'wood_for_next_lvl'):
        if inventory.wood < level.wood_for_next_lvl:
            return False
    if hasattr(level, 'skins_for_next_lvl'):
        if inventory.skins < level.skins_for_next_lvl:
            return False
    return True


def take_inv(level, inventory: Inventory):
    if hasattr(level, 'money_for_next_lvl'):
        inventory.money -= level.money_for_next_lvl
    if hasattr(level, 'wheat_for_next_lvl'):
        inventory.wheat -= level.wheat_for_next_lvl
    if hasattr(level, 'wood_for_next_lvl'):
        inventory.wood -= level.wood_for_next_lvl
    if hasattr(level, 'skins_for_next_lvl'):
        inventory.skins -= level.skins_for_next_lvl
    return inventory


def check_and_take(session: AsyncSession, gameplay):
    pass


def standart_level_up(level):
    if hasattr(level, 'money_for_next_lvl'):
        level.money_for_next_lvl = int(level.money_for_next_lvl * 1.125)
    if hasattr(level, 'wheat_for_next_lvl'):
        level.wheat_for_next_lvl = int(level.wheat_for_next_lvl * 1.125)
    if hasattr(level, 'wood_for_next_lvl'):
        level.wood_for_next_lvl = int(level.wood_for_next_lvl * 1.125)
    if hasattr(level, 'skins_for_next_lvl'):
        level.skins_for_next_lvl = int(level.skins_for_next_lvl * 1.125)

    level.time_for_next_lvl += 150
    level.cur_level += 1

    return level


def level_to_up(level):

    level = standart_level_up(level)
    if type(level) == TownSquare:
        level.time_for_citizen -= 5
        level.money_per_citizen = round(level.money_per_citizen + 0.1, 1)
        level.max_citizens += 50

    if type(level) == Bar:
        level.time_for_archer -= 5
        level.max_archers += 50

    if type(level) == Fields:
        level.res_per_worker = round(level.res_per_worker + 0.1, 1)

    if type(level) == HunterHouse:
        level.res_per_worker = round(level.res_per_worker + 0.1, 1)

    if type(level) == Market:
        level.taxes = round(level.taxes - 0.1, 1)

    if type(level) == Tower:
        pass

    if type(level) == WarHouse:
        level.time_for_knight -= 5
        level.max_knights += 50

    if type(level) == WoodHouse:
        level.time_for_res_pack -= 5
        level.res_per_worker = round(level.res_per_worker + 0.1, 1)

    return level

def check_city_name(city_name: str):
    if len(city_name) < 4:
        return "Длина названия от 4х символов"
    if len(city_name) > 16:
        return "Длина названия до 16и символов"
    return True


