import uvicorn
from fastapi import Request, Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session, async_session_maker
from sqlalchemy import select
from app.auth.models import User
from app.auth.base_config import auth_backend, fastapi_users, current_user
from app.auth.schemas import UserRead, UserCreate
from levels.router import router as router_menu
from starlette.staticfiles import StaticFiles
from app.config import templates
from app.auth.router import router as auth_router
from app.gameplay.gameplay import start_game
from contextlib import asynccontextmanager
from app.gameplay.context import make_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_game()
    yield
    pass


app = FastAPI(
    title="MEDIEVAL", lifespan=lifespan
)


app.mount("/app/static", StaticFiles(directory="static", html=True), name="static")



@app.get("/")
async def get_menu(request: Request, user: User | None = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    # try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            context = await make_context(session, user)
            return templates.TemplateResponse("menu.html", {"request": request, "context": context})
    # except:
    #     return {
    #         "status": "error",
    #         "data": ":(",
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }



@app.get("/test")
# async def test_router(request: Request, session: AsyncSession = Depends(get_async_session)):
async def test_router(request: Request):
    # Получить сессию
    session = async_session_maker()
    async with session:
        # Получить объект
        # print(await session.get(User, 1))
        # Можно делать запросы сразу с нескольких таблиц, в документации показано, как
        query = select(User).where(User.id == 1)
        pre_result = await session.execute(query)

        # print(type(pre_result))
        # различные варианты работы с resultом (который в данном случае зовется pre_result)
        # print(list(pre_result))
        # print(pre_result.fetchall())
        # print(pre_result.all())
        # print(pre_result.one())
        # Без scalars возвращает объекты в кортежах, если хочешь вытаскивать объекты из кортежей, используй scalars
        # print(pre_result.scalars().one())
        # строка ниже заменяет предыдущую
        print(pre_result.scalar_one())

        # Сешн коммит нужен только в том случае, если мы изменяли какие-либо данные внутри сессии
        # session.commit()
        # Можно использовать, чтобы удалять объекты
        # session.delete()


# Ниже стандартный способ работы с sqlalchemy
#     query = select(User).where(User.username == user)
#     pre_result = await session.execute(query)
#     result = pre_result.fetchall()
# Через select и result


# # можно использовать такую конструкцию для работы в sqla
# with async_session_maker() as session:
#     session.begin()
#     try:
#         session.add(some_object)
#         session.add(some_other_object)
#     except:
#         session.rollback()
#         raise
#     else:
#         session.commit()

# Еще более "удобный" вариант, не требующий коммита в конце
# with async_session_maker() as session, session.begin():
#     session.add(some_object)
#     session.add(some_other_object)




# Ниже два роутера - для аутентификации и регистрации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)



app.include_router(router_menu)
app.include_router(auth_router)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)



