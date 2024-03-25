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



router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)




@router.get("/{slug}")
async def get_menu_item(request: Request, slug: str, session: AsyncSession = Depends(get_async_session),  user: User | None = Depends(current_user)):
    # try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            context = await make_context(session, user, slug)
            return templates.TemplateResponse(f"menu_items/{slug}.html", {"request": request, "context": context})


    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "data": e,
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }


