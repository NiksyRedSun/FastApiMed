from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import templates

from ..database import get_async_session
from .models import Menu
# from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

#
@router.get("/{slug}")
async def get_menu_item(request: Request, slug: str, session: AsyncSession = Depends(get_async_session)):
    try:
        pre_result = await session.execute(select(Menu).where(Menu.slug==slug))
        # запомни, sqlalch всегда возвращает кортеж, поэтому в дальнейшем нужно обращаться именно к одному элементу
        result = pre_result.fetchone()
        return templates.TemplateResponse("menu_item.html", {"request": request, "menu_par": result[0]})

    except Exception as e:
        return {
            "status": "error",
            "data": e,
            "details": None
        }


