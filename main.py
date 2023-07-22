from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth, users, start_page
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user

templates = Jinja2Templates(directory='templates/')

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(start_page.router)

@app.get("/")
async def home(request: Request):
    user = await get_current_user(request)
    if user is None:
        return templates.TemplateResponse('start_page.html', {'request': request})
    return templates.TemplateResponse('start_page.html', {'request': request, 'user': user})