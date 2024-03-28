from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from config import templates
from app.auth.models import User
from app.levels.models import *
from app.auth.base_config import auth_backend, fastapi_users, current_user
from fastapi.responses import RedirectResponse
from database import get_async_session
from app.gameplay.context import make_context
from app.gameplay.gameplay import gameplays
from app.gameplay.spec_funcs import model_by_slug, check_inv




router = APIRouter(
    prefix="/level",
    tags=["level"]
)




@router.get("/{slug}")
async def get_level(request: Request, slug: str, session: AsyncSession = Depends(get_async_session),
                    user: User | None = Depends(current_user), message: str = None, message_class: str = None):
    # try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            context = await make_context(session, user, slug)
            return templates.TemplateResponse(f"menu_items/{slug}.html", {"request": request, "context": context,
                                                                          'message': message, 'message_class': message_class})


    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "data": e,
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }


@router.get("/upgrade/{slug}")
async def upgrade_level(request: Request, slug: str, session: AsyncSession = Depends(get_async_session),  user: User | None = Depends(current_user)):
    # try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            gameplay = gameplays[user.id]
            inventory = await gameplay.get_obj_by_user_id(session, Inventory)
            level = await gameplay.get_obj_by_user_id(session, model_by_slug[slug])

            if check_inv(level, inventory):
                return RedirectResponse(request.url_for('get_level', slug=slug).include_query_params(message='Улучшение запущено', message_class='success'), status_code=302)
            else:
                return RedirectResponse(request.url_for('get_level', slug=slug).include_query_params(message='Не хватает ресурсов для улучшения', message_class='error'), status_code=302)


    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "data": e,
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }


