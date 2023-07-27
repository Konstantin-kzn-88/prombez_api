import sys

sys.path.append('..')


from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'descrition': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates/')

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/account_info')
async def get_account_info(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    return templates.TemplateResponse('account_info.html', {'request': request, 'user': user})


@router.post('/account_info', response_class=HTMLResponse)
async def post_account_info(request: Request, email: str = Form(...), db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    user.email = email
    db.add(user)
    db.commit()

    msg = 'Данные изменены'
    return templates.TemplateResponse('account_info.html', {'request': request, 'user': user,  'msg': msg})