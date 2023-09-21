from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth
from routers.docs_app import account, organization, project, object, substance, device, pipeline
from routers.calc_app import explosion, strait_fire
from routers.price import price
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user

templates = Jinja2Templates(directory='templates/')

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router)
app.include_router(price.router)
app.include_router(account.router)
app.include_router(organization.router)
app.include_router(project.router)
app.include_router(object.router)
app.include_router(substance.router)
app.include_router(device.router)
app.include_router(pipeline.router)
app.include_router(explosion.router)
app.include_router(strait_fire.router)

@app.get("/")
async def home(request: Request):
    user = await get_current_user(request)
    if user is None:
        return templates.TemplateResponse('index.html', {'request': request})
    return templates.TemplateResponse('index.html', {'request': request, 'user': user})