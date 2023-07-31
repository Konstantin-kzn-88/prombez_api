import sys

import database

sys.path.append('../..')

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
    responses={404: {'descrition': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @router.get('/')
# async def get_all_projects(request: Request, db: Session = Depends(get_db)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
#     projects = db.query(models.Project).filter(models.Organization.user_id == user.get('user_id')).all()
#     return templates.TemplateResponse('docs_app/organizations.html',
#                                       {'request': request, 'organizations': organizations, 'user': user})



