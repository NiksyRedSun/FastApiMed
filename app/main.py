import uvicorn
from fastapi import APIRouter, Request, Depends, FastAPI, Form, status
from fastapi.responses import RedirectResponse
from app.auth.models import User
from app.auth.base_config import auth_backend, fastapi_users, current_user
from app.auth.schemas import UserRead, UserCreate
from app.menu.router import router as router_menu
from starlette.staticfiles import StaticFiles
from app.config import templates
from app.auth.router import router as auth_router
import nest_asyncio





app = FastAPI(
    title="MEDIEVAL"
)


app.mount("/app/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def get_menu(request: Request, user: User | None = Depends(current_user)):
    try:
        if user is None:
            return RedirectResponse(request.url_for('login_get'), status_code=302)
        else:
            return templates.TemplateResponse("menu.html", {"request": request})
    except:
        return {
            "status": "error",
            "data": ":(",
            "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
        }


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


# uvicorn app.main:app --reload

if __name__ == "__main__":
    # nest_asyncio.apply()
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)

