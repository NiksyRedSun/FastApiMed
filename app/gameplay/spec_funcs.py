from app.levels.models import *


model_by_slug = {'town_square': TownSquare, 'wood_house': WoodHouse, 'war_house': WarHouse, 'tower': Tower,
                 'market': Market, 'hhunter_house': HunterHouse, 'fields': Fields, 'bar': Bar}




def seconds_to_minutes(seconds):
    if seconds > 60:
        minutes = seconds // 60
        if minutes == 1:
            return "1 минута"
        elif 2 <= minutes <= 4:
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
            seconds = f"0{minutes}"
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
